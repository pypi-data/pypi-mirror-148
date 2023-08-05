import numpy as np
import ray
import copy
from orthrus.core.helper import batch_jobs_
from sklearn.preprocessing import StandardScaler
from typing import  Callable
def reduce_feature_set_size(ds,
                            features_dataframe, 
                            sample_ids,
                            attr:str,
                            classifier, 
                            scorer, 
                            ranking_method_handle,
                            ranking_method_args: dict,
                            partitioner=None, 
                            test_sample_ids=None,
                            start : int = 5, 
                            end : int = 100, 
                            step : int = 5, 
                            verbose_frequency : int=10, 
                            num_cpus_per_worker : float=1., 
                            num_gpus_per_worker : float=0.,
                            local_mode=False,
                            **kwargs):
    """
    This method takes a features dataframe (output of a feature selection), ranks them by a ranking method and performs 
    a feature set reduction using grid search method, which is defined by start, end and jump parameters. 

    Different training and test data may be used and the results will change accordingly. The following choices are available:
    
    if test_sample_ids is None and partitioner is None:
        
        Only training data is available, so the results will contain score on the Training data

    if test_sample_ids is not None and partitioner is None:
        
        Model is trained on all sample_ids, and then it is then evaluated on test_sample_ids. Results contain evaluation score on test_sample_ids.
    
    if test_sample_ids is None and partitioner is not None:
        
        Model is trained on partitions of sample_ids created by partitioner; results will contain the mean validation score, 
        obtained during validation on these different partitions.

    if test_sample_ids is not None and partitioner is not None:
        
        Model is trained using partitions of sample_ids defined by partitioner, and then the test_sample_ids are evaluated using all models. Results
        contain mean evaluation score on test_sample_ids.

    Args:
        features_df (pandas.DataFrame): This is a features dataframe that contains result of a feature selection. 
                                        (check orthrus.core.dataset.DataSet.feature_select method for details)

        sample_ids (like-like): List of indicators for the samples to use for training. e.g. [1,3], [True, False, True],
            ['human1', 'human3'], etc..., can also be pandas series or numpy array.

        attr (string): Name of metadata attribute to classify on.

        classifier (object): Classifier to run the classification experiment with; must have the sklearn equivalent
                of a ``fit`` and ``predict`` method.

        scorer (object): Function which scores the prediction labels on training and test partitions. This function
            should accept two arguments: truth labels and prediction labels. This function should output a score
            between 0 and 1 which can be thought of as an accuracy measure. See
            sklearn.metrics.balanced_accuracy_score for an example.

        ranking_method_handle (method handle) : handle of the feature ranking method

        ranking_method_args (dict): argument dictionary for the feature ranking method

        partitioner (object): Class-instance which partitions samples in batches of training and test split. This
            instance must have the sklearn equivalent of a split method. The split method returns a list of
            train-test partitions; one for each fold in the experiment. See sklearn.model_selection.KFold for
            an example partitioner. (default = None, check the method description above to see how this affects the results)

        test_sample_ids: List of indicators for the samples to use for testing. e.g. [1,3], [True, False, True],
            ['human1', 'human3'], etc..., can also be pandas series or numpy array. (default = None, check the method 
            description above to see how this affects the results)

        start (int): starting point of the grid search. (default: 5)
        
        end (int) :  end point of the grid search. Use -1 to set end as the size of features (default: 100)
        
        step (int) : gap between each sampled point in the grid (default: 5)

        verbose_frequency (int) : this parameter controls the frequency of progress outputs for the ray workers to console; an output is 
            printed to console after every verbose_frequency number of processes complete execution. (default: 10)
        
        num_cpus_per_worker (float) : Number of CPUs each worker needs. This can be a fraction, check 
            `ray specifying required resources <https://docs.ray.io/en/master/walkthrough.html#specifying-required-resources>`_ for more details. (default: 1.)

        num_gpus_per_worker (float) : Number of GPUs each worker needs. This can be fraction, check 
            `ray specifying required resources <https://docs.ray.io/en/master/walkthrough.html#specifying-required-resources>`_ for more details. (default: 0.)

    Return:
    
        (dict): contains 2 key-value pairs:
            'optimal_n_results': ndarray of shape (m, 2), with m being the total values sampled from the grid in the search. 
            The first column contains the number of top features (different values sampled from the grid search),  and the second 
            column contains the score.  The array is sorted by score in descending order.
        
            'reduced_feature_ids' : ndarray of shape (n, ), n is the smallest number of features, out of the m sampled values, 
            that produced the highest score. It contains reduced features ids (index of features_df).

    Example:
            >>> import orthrus.core.dataset as DS
            >>> import orthrus.sparse.feature_selection.IterativeFeatureRemoval as IFR
            
            >>> x = DS.load_dataset(file_path)
            >>> ifr = IFR.IFR(
            ...         verbosity = 2,
            ...         nfolds = 4,
            ...         repetition = 500,
            ...         cutoff = .6,
            ...         jumpratio = 5,
            ...         max_iters = 100,
            ...         max_features_per_iter_ratio = 2
            ...         )
            >>> result = x.feature_select(ifr,
                        attrname,
                        selector_name='IFR',
                        f_results_handle='results',
                        append_to_meta=False,
                        )
            >>> features_df = results['f_results']

            >>> classifier =  svm.LinearSVC(dual=False)

            >>> bsr = sklearn.metrics.balanced_accuracy_score

            >>> ranking_method_args = {'attr': 'frequency'}

            >>> partitioner = KFold(n_splits=5, shuffle=True, random_state=0)

            >>> import orthrus.sparse.feature_selection.helper as fhelper

            >>> reduced_feature_results = fhelper.reduce_feature_set_size(x, 
                                    features_df, 
                                    sample_ids_training,
                                    attrname,
                                    classifier, 
                                    bsr, 
                                    fhelper.rank_features_by_attribute,
                                    ranking_method_args,
                                    patitioner=partitioner,
                                    start = 5, 
                                    end = 100, 
                                    step = 1,
                                    verbose_frequency=10,
                                    num_cpus_per_worker=2.)

            >>> print(reduced_feature_results)
    """
    ranked_features = ranking_method_handle(features_dataframe, ranking_method_args)

    #create subset of features, from "start" to "end" in increments of "step"
    if end == -1:
        end = ranked_features.shape[0] + 1

    n_attrs = np.arange(start, end+ 1, step)

    list_of_arguments = []
    #for each subset of top features
    for i, n  in enumerate(n_attrs):
        classifier_copy = copy.deepcopy(classifier)
        arguments = [classifier_copy, 
                        ds, 
                        attr, 
                        ranked_features,
                        0,
                        n, 
                        sample_ids, 
                        scorer, 
                        partitioner, 
                        test_sample_ids,
                        kwargs]
        list_of_arguments.append(arguments)

    finished_processes = batch_jobs_(run_single_classification_experiment_, list_of_arguments, verbose_frequency=verbose_frequency,
                                                num_cpus_per_worker=num_cpus_per_worker, num_gpus_per_worker=num_gpus_per_worker, local_mode=local_mode)
    results = np.zeros((len(list_of_arguments), 2))

    for i, process in enumerate(finished_processes):
        score, feature_set_length , _ = ray.get(process)
        results[i, 0] = feature_set_length
        results[i, 1] = score
    
    # ray.shutdown()
    #find the best n, i.e. smallest n that produced largest score
    results = results[results[:,1].argsort()[::-1]]
    max_bsr = np.max(results[:, 1])
    max_bsr_idxs = np.where(results[:, 1] == max_bsr)[0]
    n = int(np.min(results[max_bsr_idxs, 0]))

    reduced_features = features_dataframe.loc[ranked_features[:n]]

    returns = {}
    returns = {'reduced_feature_ids': reduced_features.index.values,
                'optimal_n_results': results}

    return returns


def sliding_window_classification_on_ranked_features(ds, 
                            features_dataframe, 
                            sample_ids,
                            attr:str,
                            model, 
                            scorer, 
                            ranking_method_handle,
                            ranking_method_args: dict,
                            partitioner=None, 
                            test_sample_ids=None,
                            window_size = 50, 
                            stride = 5,
                            verbose_frequency : int=10, 
                            num_cpus_per_worker : float=1., 
                            num_gpus_per_worker : float=0.,
                            **kwargs):
    """
    This method takes a features dataframe (output of a feature selection), ranks them by a ranking method and performs 
    classification experiments for various feature sets, which are created by a sliding window approach defined by window size and stride. 
    The result contains score on various feature sets. Different training and test data may be used and the results change accordingly. 
    The following choices are avaible:
    
    if test_sample_ids is None and partitioner is None:
        
        Only training data is available, so the results will contain score on the Training data

    if test_sample_ids is not None and partitioner is None:
        
        Model is trained on all sample_ids, and then it is then evaluated on test_sample_ids. Results contain evaluation score on test_sample_ids.
    
    if test_sample_ids is None and partitioner is not None:
        
        Model is trained on partitions of sample_ids created by partitioner; results will contain the mean validation score, 
        obtained during validation on these different partitions.

    if test_sample_ids is not None and partitioner is not None:
        
        Model is trained using partitions of sample_ids defined by partitioner, and then the test_sample_ids are evaluated using all models. Results
        contain mean evaluation score on test_sample_ids.

    Args:
        features_df (pandas.DataFrame): This is a features dataframe that contains result of a feature selection. 
                                        (check orthrus.core.dataset.DataSet.feature_select method for details)

        sample_ids (like-like): List of indicators for the samples to use for training. e.g. [1,3], [True, False, True],
            ['human1', 'human3'], etc..., can also be pandas series or numpy array.

        attr (string): Name of metadata attribute to classify on.

        classifier (object): Classifier to run the classification experiment with; must have the sklearn equivalent
                of a ``fit`` and ``predict`` method.

        scorer (object): Function which scores the prediction labels on training and test partitions. This function
            should accept two arguments: truth labels and prediction labels. This function should output a score
            between 0 and 1 which can be thought of as an accuracy measure. See
            sklearn.metrics.balanced_accuracy_score for an example.

        ranking_method_handle (method handle) : handle of the feature ranking method

        ranking_method_args (dict): argument dictionary for the feature ranking method

        partitioner (object): Class-instance which partitions samples in batches of training and test split. This
            instance must have the sklearn equivalent of a split method. The split method returns a list of
            train-test partitions; one for each fold in the experiment. See sklearn.model_selection.KFold for
            an example partitioner. (default = None, check the method description above to see how this affects the results)

        test_sample_ids: List of indicators for the samples to use for testing. e.g. [1,3], [True, False, True],
            ['human1', 'human3'], etc..., can also be pandas series or numpy array. (default = None, check the method 
            description above to see how this affects the results)
        
        window_size (int) : The number of features to contain in each window. Default is 50. 

        stride (int) : Controls the stride of the windows. Default is 1.

        verbose_frequency (int) : this parameter controls the frequency of progress outputs for the ray workers to console; an output is 
            printed to console after every verbose_frequency number of processes complete execution. (default: 10)
        
        num_cpus_per_worker (float) : Number of CPUs each worker needs. This can be a fraction, check 
            `ray specifying required resources <https://docs.ray.io/en/master/walkthrough.html#specifying-required-resources>`_ for more details. (default: 1.)

        num_gpus_per_worker (float) : Number of GPUs each worker needs. This can be fraction, check 
            `ray specifying required resources <https://docs.ray.io/en/master/walkthrough.html#specifying-required-resources>`_ for more details. (default: 0.)

    Return:
        (ndarray of shape (num_windows, 2)):  The first column contains the starting position of the window,
        and the second column contains the score.  The array is sorted by first column in ascending order.


    Example:
            >>> import orthrus.core.dataset as DS
            >>> import orthrus.sparse.feature_selection.IterativeFeatureRemoval as IFR
            
            >>> x = DS.load_dataset(file_path)
            >>> ifr = IFR.IFR(
                verbosity = 2,
                nfolds = 4,
                repetition = 500,
                cutoff = .6,
                jumpratio = 5,
                max_iters = 100,
                max_features_per_iter_ratio = 2
                )
            >>> result = x.feature_select(ifr,
                        attrname,
                        selector_name='IFR',
                        f_results_handle='results',
                        append_to_meta=False,
                        )
            >>> features_df = results['f_results']

            >>> classifier = svm.LinearSVC(dual=False)

            >>> bsr = sklearn.metrics.balanced_accuracy_score

            >>> ranking_method_args = {'attr': 'frequency'}

            >>> partitioner = KFold(n_splits=5, shuffle=True, random_state=0)

            >>> import orthrus.sparse.feature_selection.helper as fhelper

            >>> sliding_window_results = fhelper.sliding_window_classification_on_ranked_features(x, 
                                    features_df, 
                                    sample_ids_training,
                                    attrname,
                                    classifier, 
                                    bsr, 
                                    fhelper.rank_features_by_attribute,
                                    ranking_method_args,
                                    patitioner=partitioner,
                                    window_size = 50, 
                                    stride = 5,
                                    verbose_limit=10,
                                    num_cpus_per_worker=2.0)

            >>> print(sliding_window_results)
    """
    features_dataframe = features_dataframe[features_dataframe[ranking_method_args['attr']]>0]
    ranked_features = ranking_method_handle(features_dataframe, ranking_method_args)

    n_attrs = np.arange(0, ranked_features.shape[0], stride)
    
    list_of_arguments = []
    #for each subset of top features
    for i, n  in enumerate(n_attrs):
        model_copy = copy.deepcopy(model)
        arguments = [model_copy, 
                        ds, 
                        attr, 
                        ranked_features,
                        n,
                        n+window_size, 
                        sample_ids, 
                        scorer, 
                        partitioner, 
                        test_sample_ids,
                        kwargs]
        list_of_arguments.append(arguments)

    finished_processes = batch_jobs_(run_single_classification_experiment_, list_of_arguments, verbose_frequency=verbose_frequency,
                                                num_cpus_per_worker=num_cpus_per_worker, num_gpus_per_worker=num_gpus_per_worker)
    results = np.zeros((len(list_of_arguments), 2))
    for i, process in enumerate(finished_processes):
        score, _ , min_feature_index = ray.get(process)
        results[i, 0] = min_feature_index
        results[i, 1] = score
    results = results[results[:,0].argsort()]
    # ray.shutdown()
    
    return results

@ray.remote
def run_single_classification_experiment_(model, 
                        ds, 
                        attr, 
                        features,
                        feature_start_index,
                        feature_end_index,
                        sample_ids, 
                        scorer, 
                        partitioner, 
                        test_sample_ids,
                        kwargs):
    
    features = features[feature_start_index: feature_end_index]
    
    classification_result = ds.classify(model,
                attr,
                feature_ids=features,
                sample_ids=sample_ids,
                scorer=scorer,
                partitioner=partitioner,
                **kwargs
                )

    if test_sample_ids is not None:
        ds = ds.slice_dataset(feature_ids=features, sample_ids=test_sample_ids)

        data = ds.data.values
        labels = ds.metadata[attr]

        scores = []
        for classifier in classification_result['classifiers'].values:
            predicted_labels = classifier.predict(data)
            scores.append(scorer(labels, predicted_labels))
        score = np.mean(np.array(scores))

    else:
        if partitioner is not None:
            score = np.mean(classification_result['scores'].loc['Test'].values)
        else:
            score = np.mean(classification_result['scores'].loc['Training'].values)


    return score, feature_end_index-feature_start_index, feature_start_index


def rank_features_by_attribute(features_df, args):
    """
    This method takes a features dataframe as input and ranks the features based on a numerical column/attribute.  

    Args:
        features_df (pandas.DataFrame): This is a features dataframe that contains result of a feature selection. 
                                        (check orthrus.core.dataset.DataSet.feature_select method for details)

        args (dict): This dictionary contains variables to determine which attribute to rank feature on and the
                    order of ranking. Check details for various key and values below:
                    'attr' (Mandatory): Attribute/column name from features_df to rank the features on
                    'order': Whether to rank in ascending or descending order. 'asc' for ascending and 'desc' for descending.
                             (defaul: 'desc') 
                    'feature_ids' (list-like): List of identifiers for the features to limit the ranking within certain features only. 
                            e.g. [True, False, True], ['gene1', 'gene3'], etc..., can also be pandas series or numpy array. 
                            Default: None, which corresponds to using all features.
          
    Return:
        ndarray of shape (n, )): n = number of features in feature_ids or features_df (if feature_ids is None). It contains sorted feature ids (index of features_df).

    Examples:
            >>> import orthrus.core.dataset as DS
            >>> import orthrus.sparse.feature_selection.IterativeFeatureRemoval as IFR
            
            >>> x = DS.load_dataset(file_path)
            >>> ifr = IFR.IFR(
                verbosity = 2,
                nfolds = 4,
                repetition = 500,
                cutoff = .6,
                jumpratio = 5,
                max_iters = 100,
                max_features_per_iter_ratio = 2
                )
            >>> result = x.feature_select(ifr,
                        attrname,
                        selector_name='IFR',
                        f_results_handle='results',
                        append_to_meta=False,
                        )
            >>> features_df = results['f_results']
            >>> feature_subset = features_df['frequency'] > 5
            >>> ranking_method_args = {'attr': 'frequency', feature_ids: feature_subset}
        
            feature will ranked on frequency attribute in descending and will occur only within feature_subset features.
            >>> ranked_feature_ids =  rank_features_by_attribute(features_df, ranking_method_args)
    """
    #create an array whose first column is feature indices and 
    #second column is values of the "attr" 
    if args.get('feature_ids', None) is not None:
        indices = features_df.loc[args['feature_ids']].index.values
    else:
        indices = features_df.index.values
    attr_values = features_df[args['attr']].loc[indices].values.reshape(-1,1)
    #remove features with nan values
    np.isnan(attr_values.astype(float))
    non_nan_idxs = np.invert(np.isnan(attr_values.astype(float))).reshape(-1)

    indices = np.array(indices).reshape(-1, 1)
    feature_array = np.hstack((indices, attr_values))

    feature_array = feature_array[non_nan_idxs, :]

    order=args.get('order', 'desc')
    if order=='desc':
        feature_array = feature_array[feature_array[:,1].argsort()[::-1]]
    elif order=='asc':
        feature_array = feature_array[feature_array[:,1].argsort()]
    else:
        raise ValueError('%s is an incorrect value for rank "order" in args. It should "asc" \
            for ascending or "desc" for descending.'%order)
    
    return feature_array[:, 0]


def rank_features_by_mean_attribute_value(features_df, args):
    """
    This method takes a features dataframe as input and ranks the features based on the 
    mean/meadian value a column/attribute, which contains list of numerical data.  

    Args:
        features_df (pandas.DataFrame): This is a features dataframe that contains result of a feature selection. 
                                        (check orthrus.core.dataset.DataSet.feature_select method for details)

        args (dict): This dictionary contains variables to determine which attribute to rank feature on and the
                    order of ranking. Check details for various key and values below:
                    'attr' (Mandatory): Attribute/column name from features_df to rank the features on
                    'order': Whether to rank in ascending or descending order. 'asc' for ascending and 'desc' for descending.
                             (defaul: 'desc') 
                    'feature_ids' (list-like): List of identifiers for the features to limit the ranking within certain features only. 
                            e.g. [True, False, True], ['gene1', 'gene3'], etc..., can also be pandas series or numpy array. 
                            Default: None, which corresponds to using all features.
                    'method': which operation to perform, can be "mean" or "median". (Default: "mean")
          
    Return:
        ndarray of shape (n, )): n = number of features in feature_ids or features_df (if feature_ids is None). It contains sorted feature ids (index of features_df).

    Examples:
            >>> import orthrus.core.dataset as DS
            >>> import orthrus.sparse.feature_selection.IterativeFeatureRemoval as IFR
            
            >>> x = DS.load_dataset(file_path)
            >>> ifr = IFR.IFR(
                verbosity = 2,
                nfolds = 4,
                repetition = 500,
                cutoff = .6,
                jumpratio = 5,
                max_iters = 100,
                max_features_per_iter_ratio = 2
                )
            >>> result = x.feature_select(ifr,
                        attrname,
                        selector_name='IFR',
                        f_results_handle='results',
                        append_to_meta=False,
                        )
            >>> features_df = results['f_results']
            >>> ranking_method_args = {'attr': 'selection_iteration', 'order': asc, 'method': 'median'}
            The selection_iteration column in the features_df contains a list of integer values. 
            In this example the features will be ranked by the median value of selection_iteration in ascending order.
            >>> ranked_feature_ids =  rank_features_by_mean_attribute_value(features_df, ranking_method_args)
    """
    #create an array whose first column is feature indices and 
    #second column is values of the "attr" 
    if args.get('feature_ids', None) is not None:
        indices = features_df.loc[args['feature_ids']].index.values
    else:
        indices = features_df.index.values
    
    #get values
    values = features_df[args['attr']].loc[indices].values
    method = args.get('method', 'mean')

    if method == 'mean':
        #get means
        processed_values = np.array([np.mean(np.array(x)) for x in values ]).reshape(-1, 1)
    else:
        processed_values = np.array([np.median(np.array(x)) for x in values ]).reshape(-1, 1)
    
    #get indices where values is not nan
    idx = np.where(np.isnan(processed_values) == False)[0]
    
    indices = np.array(indices).reshape(-1, 1)
    feature_array = np.hstack((indices, processed_values))
    feature_array = feature_array[idx, :]

    order=args.get('order', 'desc')
    if order=='desc':
        feature_array = feature_array[feature_array[:,1].argsort()[::-1]]
    elif order=='asc':
        feature_array = feature_array[feature_array[:,1].argsort()]
    else:
        raise ValueError('%s is an incorrect value for rank "order" in args. It should "asc" for ascending or "desc" for descending.'%order)
    
    return feature_array[:, 0]


def rank_features_within_attribute_class(features_df, 
                                    feature_class_attribute, 
                                    new_feature_attribute_name,
                                    x, 
                                    partitioner, 
                                    sample_ids,
                                    scorer,
                                    classification_attr,
                                    classifier_factory_method,
                                    f_weights_handle,
                                    feature_ids = None,
                                    **kwargs):
    features_df[new_feature_attribute_name] = 0

    if feature_ids is None:
        feature_ids = features_df.index
    #get unique values (classes) for the attributes
    unique_attr_values = np.unique(features_df[feature_class_attribute].loc[feature_ids].values)
    unique_attr_values = np.sort(unique_attr_values)[::-1]
    for val in unique_attr_values:
        features = features_df[feature_class_attribute] == val
        if features.sum() != 1:    

            #train model on the features for the current class
            classififer = classifier_factory_method()
            results = x.classify(classififer,
                        classification_attr,
                        feature_ids=features,
                        sample_ids=sample_ids,
                        partitioner=partitioner,
                        scorer=scorer,
                        f_weights_handle = f_weights_handle)

            #extract mean of absolute weights for features
            weights_keys = results['f_weights'].keys()
            filtered_keys = [k for k in weights_keys if 'weights' in k]            
            weights = results['f_weights'][filtered_keys].values
            mean_of_abs_weights = np.mean(np.abs(weights), axis=1)

            #normalize features between 0 and 1
            
            b = .999
            a = .001
            r_max = np.max(mean_of_abs_weights)
            r_min = np.min(mean_of_abs_weights)
            mean_of_abs_weights = (b-a) * (mean_of_abs_weights - r_min) / (r_max - r_min) + a
            mean_of_abs_weights = val + mean_of_abs_weights
        else:
            mean_of_abs_weights = val
            
        features_df.loc[features, new_feature_attribute_name] = mean_of_abs_weights

def get_batch_correction_matric_for_ranked_features(ds, 
                            features_dataframe, 
                            attr:str,
                            ranking_method_handle,
                            ranking_method_args: dict,
                            batch_correction_metric_handle,
                            batch_correction_metric_args: dict,
                            sample_ids: None,
                            verbose_frequency : int=10, 
                            num_cpus_per_worker : float=1., 
                            num_gpus_per_worker : float=0.,):
    
    ranked_features = ranking_method_handle(features_dataframe, ranking_method_args)

    if sample_ids is None:
        sample_ids = ds.data.index

    n_attrs = np.arange(1, ranked_features.shape[0])
    features = ds.vardata.index.values
    print('Starting batch correction metric computation. There are %d processes to execute.'%n_attrs.shape[0])
    list_of_arguments = []
    #for each subset of top features
    for i, n  in enumerate(n_attrs):
        feature_ids = np.delete(features, ranked_features[:n])
        arguments = [ds,
                    sample_ids,
                    feature_ids,
                    attr, 
                    batch_correction_metric_args]
        list_of_arguments.append(arguments)

    finished_processes = batch_jobs_(batch_correction_metric_handle, list_of_arguments, verbose_frequency=verbose_frequency,
                                                num_cpus_per_worker=num_cpus_per_worker, num_gpus_per_worker=num_gpus_per_worker)
    results = np.zeros((len(list_of_arguments), 2))
    n_features = features.shape[0]
    for i, process in enumerate(finished_processes):
        n, _ , _, rejection_rate = ray.get(process)
        results[i, 0] = n_features - n
        results[i, 1] = rejection_rate
    
    # ray.shutdown()
    
    #sort results based on the first column: number of ranked features
    results = results[results[:,0].argsort()]

    return results

def  get_top_95_features(file, attr, cutoff_fraction=0.05):
    from orthrus.core.helper import load_object
    if type(file) == str:
        result = load_object(file)
    else:
        result = file
    ranking_method_args = {'attr': attr, 'order': 'desc'}
    ranked_feature_ids = rank_features_by_attribute(result['f_results'], ranking_method_args)

    features = result['f_results'].loc[ranked_feature_ids]
    max_val = features[attr].max()
    cutoff = max_val * cutoff_fraction
    features_c = features.loc[features[attr] > cutoff]
    return features_c

def get_correlates(S, X, c):
    """
    This function takes a list of feature indices and a data matrix and returns the features from ``X`` which have
    correlation in absolute at least ``c``.

    Args:
        S (array-like of shape (n_important_features,): Feature indices of featues to be correlated to.
        X (array-like of shape (n_samples, n_features)): Data matrix with features.
        c (float): Correlation threshold.

    Returns:
        (ndarray) : Correlated features.
    """

    # convert indices to bool
    s = (np.array(S).reshape(-1, 1) == np.arange(X.shape[1])).any(axis=0)
    T = np.where(~s)[0]

    # compute the correlation matrix
    C = np.corrcoef(X.T)
    C = C[s, :]
    C = C[:, ~s]

    # threshold the correlations
    C = np.abs(C) >= c
    return T[C.any(axis=0)]

def plot_feature_frequency(f_ranks, attr):
    import matplotlib.pyplot as plt
    ranked_feature_ids = rank_features_by_attribute(f_ranks, {'attr': attr, 'order': 'desc'})
    f_ranks = f_ranks.loc[ranked_feature_ids]
    f_ranks = f_ranks.loc[f_ranks[attr] > 0]
    fig, axs = plt.subplots(1,1)
    axs.plot(np.arange(len(f_ranks)), f_ranks[attr].values)
    axs.set_ylabel("Frequency")
    axs.set_xlabel("Feature index")
    # axs.set_title(labels[tranfrom_id])
    plt.show()



from orthrus.core.pipeline import Transform
from orthrus.core.dataset import DataSet
class ReduceIFRFeatures(Transform):
    def __init__(self,
                #  process: object,
                 supervised_attr:str,
                 classifier,
                 scorer,
                 ranking_method_handle,
                 ranking_method_args: dict,
                 parallel: bool = False,
                 verbosity: int = 1,
                 partitioner=None,
                 start : int = 5,
                 end : int = 100,
                 step : int = 5,
                 verbose_frequency : int=10,
                 num_cpus_per_worker : float=1.,
                 num_gpus_per_worker : float=0.,
                 local_mode=False, 
                 fit_args=None):
        
        # init with Process class
        super(ReduceIFRFeatures, self).__init__(process=None,
                                        process_name='ReduceIFRFeatures',
                                        parallel=False,
                                        verbosity=verbosity,
                                        )
        self.supervised_attr = supervised_attr
        self.classifier = classifier
        self.scorer = scorer
        self.ranking_method_handle = ranking_method_handle
        self.ranking_method_args = ranking_method_args
        self.parallel = parallel
        self.verbosity = verbosity
        self.partitioner = partitioner
        self.start  = start
        self.end = end
        self.step = step
        self.verbose_frequency = verbose_frequency
        self.num_cpus_per_worker = num_cpus_per_worker
        self.num_gpus_per_worker = num_gpus_per_worker
        self.local_mode = local_mode
        self.fit_args = fit_args

    def _run(self, ds: DataSet, **kwargs) -> dict:

        ds = self._preprocess(ds, **kwargs)
        features_df = kwargs['f_ranks']

        sample_ids =  self._extract_training_ids(ds, **kwargs)
        results_ = reduce_feature_set_size(ds,
                            features_df,
                            sample_ids,
                            self.supervised_attr,
                            self.classifier,
                            self.scorer,
                            self.ranking_method_handle,
                            self.ranking_method_args,
                            partitioner=self.partitioner,
                            start=self.start,
                            end=self.end,
                            step=self.step,
                            verbose_frequency=self.verbose_frequency,
                            num_cpus_per_worker = self.num_cpus_per_worker,
                            num_gpus_per_worker = self.num_gpus_per_worker,
                            local_mode=self.local_mode
                            )
        results_['transform'] = self._generate_transform(self, results_['reduced_feature_ids'])
        return results_
    # def _fit_transform(self, ds: DataSet, **kwargs) -> Tuple[object, DataSet]:

    def _generate_transform(self, process: object, reduced_feature_ids) -> Callable:

        # define transform
        def transform(ds: DataSet):
            ds_new = ds.slice_dataset(feature_ids=reduced_feature_ids)
            return ds_new

        return transform
