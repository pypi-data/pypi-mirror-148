# from __future__ import absolute_import, division, print_function
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import random
from calcom.solvers import LPPrimalDualPy
import copy 
from sklearn.metrics import balanced_accuracy_score
from orthrus.core.helper import batch_jobs_
import ray

class IFR:

    """
    The Iterative Feature Removal algorithms extracts features for many data partitions independently, and combines 
    them and keep track of feature frequency, weights and iterations in which each feature was extracted. During execution, 
    the data is partitioned into training and validation sets 'repetition' number of times and then for each partition
    one feature set is extracted. So, a total of repetition * num_partitions independent feature sets are extracted 
    and the results are merged to create the output. These independent feature set extractions are batched 
    and run in parallel using the `ray` package. Each feature extraction is a ray worker, see below to check how to specify 
    resource requirements for each worker.
    
    For each feature set, the algorithm can halt because of the following conditions:

        1. Score on validation partition is below cutoff 
        2. Jump does not occur in the array of sorted absolute weights
        3. Jump occurs but the weight at the jump is too small ( < 10e-6)
        4. Number of features selected for the current iteration is greater than max_features_per_iter_ratio * num_samples in training partition. This condition prevents overfitting.
        5. max_iters number of iterations complete successfully

    When one of these conditions happen, further feature extraction on the current fold is stopped.

    Parameters:
        classifier (object): Classifier to run the classification experiment with; must have the sklearn equivalent
                of a ``fit`` and ``predict`` method. Default classifier is orthrus.sparse.classifiers.svm .SSVMClassifier, it will
                be a CPU based classifier if ``num_gpus_per_worker`` is 0, otherwise it will be a GPU classifier.

        scorer (object): Function which scores the prediction labels on training and test partitions. This function
            should accept two arguments: truth labels and prediction labels. This function should output a score
            between 0 and 1 which can be thought of as an accuracy measure. See
            sklearn.metrics.balanced_accuracy_score for an example.

        weights_handle (str) : Name of ``classifier`` attribute containing feature weights. Default is 'weights_'.

        repetition (int): Determines the number of times to partition the dataset. (default: 10)
        
        partition_method (string): A partition method that is compatible with calcom.utils.generate_partitions (default: 'stratified_k-fold')

        nfolds (int): The number of folds to partition data into (default: 3)

        max_iters (int): Determines the maximum number of iterations of IFR on one data partition(default: 5)
        
        cutoff (float): Threshold for the validation score to halt the process. (default: 0.75)

        jumpratio (float): The relative drop in the magnitude of coefficients in weight vector to identify numerically zero weights (default: 100)

        max_features_per_iter_ratio (float) : A fraction that limits the max number of features that can be extracted per iteration. (default: 0.8)
            if the number if selected features is greater than max_features_per_iter_ratio * #samples in training partition, further execution
            on the current fold is stopped.

        verbosity (int) : Determines verbosity of print statments; 0 for no output; 2 for full output. (default: 0)
        
        verbose_frequency (int) : this parameter controls the frequency of progress outputs for the ray workers to console; an output is 
            printed to console after every verbose_frequency number of processes complete execution. (default: 10)

        num_cpus_per_worker (float) : Number of CPUs each worker needs. This can be a fraction, check 
            `ray specifying required resources <https://docs.ray.io/en/master/walkthrough.html#specifying-required-resources>`_ for more details. (default: 1.)

        num_gpus_per_worker (float) : Number of GPUs each worker needs. This can be fraction, check 
            `ray specifying required resources <https://docs.ray.io/en/master/walkthrough.html#specifying-required-resources>`_ for more details. (default: 0.)
                
    Attributes:
        diagnostic_information_ (dict): Holds execution the following information for each interation of each partition.
            'train_scores' (list) : Each element is a list of training scores for the feature selection on one data partatition, 
                                    the number of elements in this inner list is the number of iterations IFR ran for, for this particular data partition. 

            'validation_scores' (list): Each element is a list of test scores for the feature selection on one data partatition, 
                                    the number of elements in this inner list is the number of iterations IFR ran for, for this particular data partition.  

            'sorted_abs_weights (list)': Each element is a list of sorted absolute weights for the classifier for the feature selection on one data partatition, 
                                    the number of elements in this inner list is the number of iterations IFR ran for, for this particular data partition.   

            'weight_ratios' (list)': Each element is a list of weight ratios for the classifier for the feature selection on one data partatition, 
                                    the number of elements in this inner list is the number of iterations IFR ran for, for this particular data partition.   

            'features' (list)': Each element is a list of selected feature ids for the feature selection on one data partatition, 
                                    the number of elements in this inner list is the number of iterations IFR ran for, for this particular data partition.   

            'true_feature_count' (list): Each element is a list of true number of features that IFR determined were to be selected for the feature selection on one data partatition, 
                                    the number of elements in this inner list is the number of iterations IFR ran for, for this particular data partition. 

            'exit_reasons' (list): Each element contains the reason for why the IFR stopped for the feature selection on one data partatition. These are one of the following reasons:
                1. exception_in_model_fitting
                2. validation_score_cutoff: Score on validation partition is below cutoff 
                3. jump_failed: Jump does not occur in the array of sorted absolute weights
                4. small_weight_at_jump: Jump occurs but the weight at the jump is too small ( < 10e-6)
                5. max_features_per_iter_breached: Number of features selected for the current iteration is greater than max_features_per_iter_ratio * num_samples in training partition. This condition prevents overfitting.
                6. max_iters: max_iters number of iterations complete successfully




    Examples:
            >>> import orthrus.core.dataset as DS
            >>> import orthrus.sparse.feature_selection.IterativeFeatureRemoval as IFR
            >>> x = DS.load_dataset('path/to/gse_730732.h5')
            >>> from calcom.solvers import LPPrimalDualPy
            >>> import calcom
            >>> model = calcom.classifiers.SSVMClassifier()
            >>> model.params['C'] = 1.
            >>> model.params['method'] = LPPrimalDualPy
            >>> model.params['use_cuda'] = True
            >>> weights_handle="results['weight']"
            >>> ifr = IFR.IFR(
                model,
                weights_handle=weights_handle,
                repetition = 50,
                nfolds = 4,
                max_iters = 100,
                cutoff = .6,
                jumpratio = 5,
                max_features_per_iter_ratio = 2,
                verbosity = 2,
                num_gpus_per_worker=0.1
                )

            >>> #see feature select method for details
            >>> result = x.feature_select(ifr,
                        attrname,
                        selector_name='IFR',
                        f_results_handle='results',
                        append_to_meta=False,
                        )
    
    See :py:meth:`IFR.fit` to understand the output of `IFR`.
    """
    def __init__(self,
                classifier = None,
                scorer = balanced_accuracy_score,
                weights_handle: str ='weights_',
                repetition: int=10,
                partition_method: str = 'stratified_k-fold',
                nfolds: int = 3,
                max_iters: int=5,
                cutoff: float=0.75,
                jumpratio: float=100.,
                max_features_per_iter_ratio: float=0.8,
                verbosity: int=0,
                verbose_frequency: int=10,
                num_cpus_per_worker: float=1.,
                num_gpus_per_worker: float=0.,
                local_mode=False):

        self.num_cpus_per_worker = num_cpus_per_worker
        self.num_gpus_per_worker = num_gpus_per_worker

        if classifier == None:
            from orthrus.sparse.classifiers.svm import SSVMClassifier
            if self.num_gpus_per_worker == 0:
                use_cuda = False
            elif self.num_gpus_per_worker > 0:
                use_cuda  = True
            classifier = SSVMClassifier(C=1, solver=LPPrimalDualPy, use_cuda=use_cuda)
        
        self.classifier = classifier
        self.scorer = scorer
        self.weights_handle = weights_handle
        self.repetition = repetition   # Number of time the data is randomly partitioned.
        self.partition_method =  partition_method # Passed to calcom.utils.generate_partitions
        self.nfolds = nfolds   # Passed to calcom.utils.generate_partitions
        self.max_iters = max_iters    # Max iterations for IFR on one data partition
        self.cutoff = cutoff    # validation score threshold
        self.jumpratio = jumpratio # Relative drop needed to detect numerically zero weights in SSVM.
        self.max_features_per_iter_ratio = max_features_per_iter_ratio   # fraction of training data samples as cutoff for maximum features extracted per iteration 
        self.verbosity = verbosity    # Verbosity of print statements; make positive to see detail.
        self.verbose_frequency = verbose_frequency
        self.local_mode = local_mode


        self.diagnostic_information_ = {}
        self._diagnostic_information_keys = ['train_scores', 'validation_scores', 'sorted_abs_weights', 'weight_ratios',
                                            'features', 'true_feature_count']
        self._initialize_diagnostic_dictionary(self.diagnostic_information_)
        self.diagnostic_information_['exit_reasons'] = []
        super(IFR, self).__init__()
    #

    def _initialize_diagnostic_dictionary(self, diag_dict):
        for key in self._diagnostic_information_keys:
            diag_dict[key] = []
       
    def _add_diagnostic_info_for_current_iteration(self, diag_dict, train_score, validation_score,
        sorted_abs_weights, weight_ratios, features, true_feature_count):

        diag_dict.get('train_scores', []).append(train_score)
        diag_dict.get('validation_scores', []).append(validation_score)
        diag_dict.get('sorted_abs_weights', []).append(sorted_abs_weights)
        diag_dict.get('weight_ratios', []).append(weight_ratios)
        diag_dict.get('features', []).append(features)
        diag_dict.get('true_feature_count', []).append(true_feature_count)


    def _sanity_check_diagnostics(self, diag_dict, n_iters):
        arr = np.zeros(len(self._diagnostic_information_keys))
        for i, key in enumerate(self._diagnostic_information_keys):
            arr[i] = len(diag_dict[key])

        assert np.unique(arr).shape[0] == 1, 'Lenghts of lists for the diagnostic information do not match. They should be of same size' 
        if n_iters > 1:
            assert np.unique(arr)[0] == n_iters, 'diagnostic dictionary does not contain all the information'

    def _add_diagnostic_info_for_data_partition(self, diag_dict, n_data_partition, exit_reason):
        for key in self._diagnostic_information_keys:
            self.diagnostic_information_[key].append(diag_dict[key])
        
        self.diagnostic_information_['exit_reasons'].append(exit_reason)

    
    def _initialize_results(self, n_attributes):
        '''
        Initializes self.results_ attribute
        '''
        self.results_ = pd.DataFrame(index=np.arange(n_attributes))
        self.results_['frequency'] = 0
        self.results_['weights'] = np.empty((len(self.results_), 0)).tolist() 
        self.results_['selection_iteration'] = np.empty((len(self.results_), 0)).tolist() 


    def _update_frequency_in_results(self, features):
        '''
        Increments the values of features by 1, for passed features, in frequency column of self.results_
        '''
        self.results_.loc[features, 'frequency'] =  self.results_.loc[features, 'frequency'] + 1


    def _update_selection_iteration_in_results(self, list_of_features):
        '''
        Appends the iteration number, for passed features, in selection_iteration column of self.results_
        '''
        for iteration, features in enumerate(list_of_features):
            for feature in features:
                iter_list = self.results_.loc[feature, 'selection_iteration']
                iter_list.append(iteration)

    def _update_weights_in_results(self, features, weights):
        '''
        Appends the weight for passed features in the weights column in self.results_
        ''' 
        #iterate over features
        for feature, weight in zip(features, weights):
            #append the weight to the list of weights for the current feature
            weights = self.results_.loc[feature, 'weights']
            weights.append(weight)
            
    def fit(self, data, y):
        '''
        Args:
        data (ndarray of shape (m, n))): array of data, with m the number of observations in R^n.
        y (ndarray of shape (m))): vector of labels for the data

        Return:
        (pandas.DataFrame) : The dataframe contains the results of IFR. It is indexed by feature_ids and each column 
        contains different information for each feature as described below:

            * frequency \: How many times the feature is extracted
            * weights \: Contains a list of weights, from the weight vectors during training on different partitions. 
              Each value corresponds to the weight for the feature over different extractions. The length of the weights 
              is equal to the frequency.
            * selection_iteration \: Contains a list of indices of the iteration when the feature was extracted over 
              different data partitions. The length of the list is equal to the frequency.
        '''
        import calcom
        import numpy as np
        from pandas import DataFrame, Series

        if type(y) == Series:
            y  = y.values
        
        if type(data) == DataFrame:
            data  = data.values

        m,n = np.shape(data)

        if self.verbosity>0:
            print('IFR parameters:\n')
            print('repetition', self.repetition)
            print('partition_method', self.partition_method)
            print('nfolds', self.nfolds)
            print('max_iters', self.max_iters)
            print('jumpratio', self.jumpratio)
            print('cutoff', self.cutoff)
            print('max_features_per_iter_ratio', self.max_features_per_iter_ratio)
            print('verbosity', self.verbosity)
            print('\n')
        #

        if self.nfolds < 2:
            raise ValueError("Number of folds have to be greater than 1")

        self._initialize_results(n)

        n_data_partition = 0
        list_of_arguments = []
        # start processing
        for n_rep in range(self.repetition):

            partitions = calcom.utils.generate_partitions(y, method=self.partition_method, nfolds=self.nfolds)

            for i, partition in enumerate(partitions):

                n_data_partition +=1

                train_idx, validation_idx = partition
                train_data = data[train_idx, :]
                train_labels = y[train_idx]

                validation_data = data[validation_idx, :]
                validation_labels = y[validation_idx]
                
                arguments = [self,
                            train_data,
                            validation_data,
                            train_labels,
                            validation_labels]

                list_of_arguments.append(arguments)

        
        finished_processes = batch_jobs_(self.select_features_for_data_partition, list_of_arguments, verbose_frequency=self.verbose_frequency,
                                        num_cpus_per_worker=self.num_cpus_per_worker, num_gpus_per_worker=self.num_gpus_per_worker, local_mode=self.local_mode)

        for process in finished_processes:
            results = ray.get(process)
            # update the feature set dictionary based on the features collected for current fold
            list_of_features_for_curr_fold = results['list_of_features']
            self._update_frequency_in_results(list_of_features_for_curr_fold)
            
            list_of_weights_for_curr_fold = results['list_of_weights']
            self._update_weights_in_results(list_of_features_for_curr_fold, list_of_weights_for_curr_fold) 
            list_of_selection_iterations_for_current_fold = results['list_of_selection_iteration']
            self._update_selection_iteration_in_results(list_of_selection_iterations_for_current_fold)   
            
            n_iters = results['n_iters']
            diagnostic_info_dictionary = results['diagnostic_info_dictionary']
            exit_reason = results['exit_reason']
                            
            self._sanity_check_diagnostics(diagnostic_info_dictionary, n_iters)
            #save the diagnostic information for this data partition
            self._add_diagnostic_info_for_data_partition(diagnostic_info_dictionary, n_data_partition, exit_reason)
            #

        if self.verbosity>0:
            print("=====================================================")
            print("Finishing Execution. %d features out of a total of %d features were selected."% ((self.results_['frequency'] > 0).sum(), data.shape[1]))
            print("=====================================================")
        # ray.shutdown()
        return self

    @ray.remote
    def select_features_for_data_partition(self, train_data, validation_data, train_labels, validation_labels):
        n_original_train_samples, n = train_data.shape

        from imblearn.over_sampling import SMOTE
        labels, counts = np.unique(np.array(train_labels), return_counts=True)
        sm = SMOTE({labels[0]:50, labels[1]: 50}, k_neighbors=2)
        
        train_data, train_labels = sm.fit_resample(train_data, train_labels)
      
        #resample original number of training samples from surrogate data
        x_train = np.empty((n_original_train_samples, n))
        y_train = np.empty((n_original_train_samples))

        i = 0
        for label, count in zip(labels,counts):
            idxs = np.where(train_labels==label)[0]
            np.random.shuffle(idxs)
            idxs = idxs[:count]
            x_train[i:i+count] = train_data[idxs, :]
            y_train[i:i+count] = train_labels[idxs]
            i += count

        assert np.linalg.matrix_rank(train_data) == n_original_train_samples, 'rank of subsampled matrix is less than %d'%n_original_train_samples
        train_data = x_train
        train_labels = y_train

        list_of_features_for_curr_fold = np.array([], dtype=np.int64)
        list_of_weights_for_curr_fold = np.array([], dtype=np.int64)  
        list_of_selection_iterations_for_current_fold = []

        selected = np.array([], dtype=np.int64)
        # Mask array which tracks features which haven't been removed.
        active_mask = np.ones(n, dtype=bool)

        #create an empty dictionary to store diagnostic info for the
        #current data partition, this dictionary has info about each iteration
        #on the current data partition
        diagnostic_info_dictionary = {}
        self._initialize_diagnostic_dictionary(diagnostic_info_dictionary)
        exit_reason = "max_iters"
        num_selected_features = np.array([-1] * 10)
        for i in range(self.max_iters):
            if self.verbosity > 1:
                print("=====================================================")
                print("beginning of inner loop iteration ", i+1)
                print("Number of features selected for this fold: %i of %i"%(len(list_of_features_for_curr_fold), n))
                print("Checking score of complementary problem... ",end="")
            #

            #create a copy of the classifier
            model = copy.deepcopy(self.classifier)

            tr_d = np.array( train_data[:,active_mask] )
            te_d = np.array( validation_data[:,active_mask] )
            try:
                model.fit(tr_d, train_labels)
            except Exception as e:
                if self.verbosity>0:
                    print("Warning: during the training process the following exception occurred:\n")
                    print(str(e))
                    print("\nBreaking the execution for the current data fold")
                    #save the diagnostic information
                    
                self._add_diagnostic_info_for_current_iteration(diagnostic_info_dictionary,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None)
                exit_reason = "exception_in_model_fitting"
                break
            
            weight = eval("model" + "." + self.weights_handle)

            #calculate score for training data
            pred_train = model.predict(tr_d)
            score_train = self.scorer(train_labels, pred_train)

            ##########
            #
            # Detect where the coefficients in the weight vector are
            # numerically zero, based on the (absolute value) ratio of
            # successive coefficients.
            #

            # Look at absolute values and sort largest to smallest.
            abs_weights = (np.abs(weight)).flatten()
            order = np.argsort(-abs_weights)
            sorted_abs_weights = abs_weights[order]

            # Detect jumps in the coefficient values using a ratio parameter.
            weight_ratios = sorted_abs_weights[:-1] / (sorted_abs_weights[1:] + np.finfo(float).eps)
            jumpidxs = np.where(weight_ratios > self.jumpratio)[0]

            if self.verbosity>1:
                print('')
                print("Training Score %.3f. "%score_train)
                print("")

            #calculate score for validation data
            pred_validation = model.predict(te_d)
            score_validation = self.scorer(validation_labels, pred_validation)

            if self.verbosity>1:
                print("Validation Score %.3f. "%score_validation)
                print("")

            #Check if score is above cutoff
            if (score_validation < self.cutoff):
                if self.verbosity>1:
                    print("Validation score below cutoff, exiting inner loop.")

                #save the diagnostic information for this iteration
                #in this case we only have train and validation score
                self._add_diagnostic_info_for_current_iteration(diagnostic_info_dictionary,
                    score_train,
                    score_validation,
                    sorted_abs_weights,
                    weight_ratios,
                    None,
                    None)

                #break out of current loop if score is below cutoff
                exit_reason = "validation_score_cutoff"
                break




            #check if sufficient jump was found
            if len(jumpidxs)==0:
                #jump never happened.
                #save the diagnostic information for this iteration
                #we still do not have the selected feature count and features

                self._add_diagnostic_info_for_current_iteration(diagnostic_info_dictionary,
                    score_train,
                    score_validation,
                    sorted_abs_weights,
                    weight_ratios,
                    None,
                    None)
                exit_reason = "jump_failed"
            
            
                #break out of the loop
                if self.verbosity>1:
                    print('There was no jump of sufficient size between ratios of successive coefficients in the weight vector.')
                    print("Discarding iteration..")
                break

            else:
                count = jumpidxs[0]

            #check if the weight at the jump is greater than cutoff
            if sorted_abs_weights[count] < 1e-6:

                self._add_diagnostic_info_for_current_iteration(diagnostic_info_dictionary,
                    score_train,
                    score_validation,
                    sorted_abs_weights,
                    weight_ratios,
                    None,
                    None)
                exit_reason = "small_weight_at_jump"
                if self.verbosity>1:
                    print('Weight at the jump(', sorted_abs_weights[count] ,')  smaller than weight cutoff(1e-6).')
                    print("Discarding iteration..")
                break

            count += 1

            #check if the number of selected features is greater than the cap
            if count < n_original_train_samples -1:
                #select features: order is list of sorted features
                print('selected less features than max features cutoff')
                selected = order[:count]
            else:
                print('Selected features more than cutoff. Picking random feature.')
                idx = np.random.randint(count)
                selected = order[idx:idx+1]

            num_selected_features = np.roll(num_selected_features, -1)
            num_selected_features[-1] = count

            last_ten_same = np.unique(num_selected_features).shape[0] == 1
            if count > n_original_train_samples or last_ten_same:

                self._add_diagnostic_info_for_current_iteration(diagnostic_info_dictionary,
                    score_train,
                    score_validation,
                    sorted_abs_weights,
                    weight_ratios,
                    None,
                    None)
                exit_reason = "max_features_per_iter_breached"
                if self.verbosity>1:
                    print('%d features selected, when training data has %d samples('%(count, train_data.shape[0]-1))
                    print("Discarding iteration..")
                
                break
 


            if self.verbosity>1:
                print("\nSelected features on this iteration:")
                print(selected)
                print("\n")
            #

            # Selected indices are relative to the current active set.
            # Get the mapping back to the original indices.
            active_idxs = np.where(active_mask)[0]

            active_mask[active_idxs[selected]] = 0

            #append the selected features to the list_of_features_for_curr_fold
            list_of_features_for_curr_fold = np.concatenate([list_of_features_for_curr_fold ,  active_idxs[selected]])
            list_of_weights_for_curr_fold = np.concatenate([list_of_weights_for_curr_fold ,  weight.flatten()[order][:count]])
            #save the diagnostic information for this iteration
            #here we have all the information we need
            self._add_diagnostic_info_for_current_iteration(diagnostic_info_dictionary,
                score_train,
                score_validation,
                sorted_abs_weights,
                weight_ratios,
                active_idxs[selected],
                count)

            if self.verbosity>1:
                print('Removing %i features from training and validation matrices.'%len(selected))
                print("\n")

            #append the selection iterations for the features selected in the current iteration
            list_of_selection_iterations_for_current_fold.append(active_idxs[selected])
        
        results = {}
        results['list_of_features'] = list_of_features_for_curr_fold
        results['list_of_weights'] = list_of_weights_for_curr_fold
        results['list_of_selection_iteration'] = list_of_selection_iterations_for_current_fold
        results['diagnostic_info_dictionary'] = diagnostic_info_dictionary
        results['exit_reason'] = exit_reason
        results['n_iters'] = i+1
        return results 


    def transform(self, features, **kwargs):
        return self.results_['frequency'] > 0

    def plot_basic_diagnostic_stats(self, validation_score_iteration_idx = None, n_random_exp = -1, exit_reason = ''):
        exit_reasons = self.diagnostic_information_['exit_reasons']
        #self.diagnostic_information_.pop('exit_reasons')

        fig, axs = plt.subplots(figsize=(12, 4), nrows = 2, ncols = 4)
        if exit_reason == '':
            n_elements = len(self.diagnostic_information_['validation_scores'])
            idx = np.arange(n_elements)
        else:
            idx = np.where(np.array(self.diagnostic_information_['exit_reasons']) == exit_reason)[0]
        random.shuffle(idx)

        if n_random_exp != -1 and n_random_exp < idx.shape[0]:
            idx = idx[:n_random_exp]

        axs[0][0].set_title('validation score')
        axs[0][0].set_ylim(0, 1.1)
        axs[0][1].set_title('Features Selected')
        max_iters = 0
        for j in idx:    
            num_iters = len(self.diagnostic_information_['validation_scores'][j])
            if num_iters == 1:
                axs[0][0].plot(0, self.diagnostic_information_['validation_scores'][j], marker='.', alpha = 0.5)
            else:
                axs[0][0].plot(self.diagnostic_information_['validation_scores'][j], alpha = 0.5)
            #axs[i, 0].plot(0, dict['cutoff'], len(dict['validation_score']), dict['cutoff'])
            if max_iters < num_iters:
                max_iters = num_iters

            axs[0][1].plot(self.diagnostic_information_['true_feature_count'][j], alpha = 0.5)
            #axs[i, 1].plot(0, dict['max_features_per_iter_ratio'], len(dict['validation_score']), dict['max_features_per_iter_ratio'])

        axs[0][0].set_xlim(-.9, max_iters + 1)
        exit_r = np.array(exit_reasons)
        n_elements = np.unique(exit_r).shape[0]
        
        axs[0][2].hist(exit_reasons, n_elements, histtype='stepfilled', facecolor='g', alpha=0.75)
        axs[0][2].set_title('Exit Reasons')


        #second row of plots

        #first plot shows the histogram of number of iterations
        num_iterations = np.array([len(x) for x in self.diagnostic_information_['true_feature_count']])
        axs[1][0].hist(num_iterations)
        axs[1][0].set_ylabel('Frequency')
        axs[1][0].set_xlabel('# Iterations per partition')

        #second plot show the histogram of validation scores
        if validation_score_iteration_idx == None:
            validation_scores = [item for sublist in self.diagnostic_information_['validation_scores'] for item in sublist]
            label = 'Validation Scores over all iterations and partition'
        else:
            validation_scores = []
            for sublist in self.diagnostic_information_['validation_scores']:
                if len(sublist) >= validation_score_iteration_idx:
                    validation_scores = validation_scores.append(sublist[validation_score_iteration_idx])
            label = 'Validation Scores over iteration# %d of all partition'%validation_score_iteration_idx
        axs[1][1].hist(validation_scores)
        axs[1][1].set_ylabel('Frequency')
        axs[1][1].set_xlabel(label)

        weight_ratios = np.array(self.diagnostic_information_['weight_ratios'])
        sorted_abs_weights = np.array(self.diagnostic_information_['sorted_abs_weights'])
        #find partitions where the first iteration extracted features (did not fail because of some condition)
        if exit_reason == '':
            idxs = np.where(np.array([len(x) >= 1 for x in weight_ratios]) == True)[0]
            which = 0
        else:
            idxs = np.where(np.array(self.diagnostic_information_['exit_reasons']) == exit_reason)[0]
            which = -1
        print(idxs)
        random.shuffle(idxs)
        idxs = idxs[:n_random_exp]
        
        for idx in idxs:
            for j in range(len(weight_ratios[idx])):
                axs[1][2].plot(weight_ratios[idx][j][:20])
                axs[1][3].plot(sorted_abs_weights[idx][j][:20])
        axs[1][2].set_ylabel('weight ratios')
        axs[1][3].set_ylabel('sorted absolute weights')


        plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
        plt.show()

#