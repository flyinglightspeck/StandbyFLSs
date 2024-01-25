# Standby FLSs for FLS Illumination

## Python Version
This software was developed based on Python 3.9.0

## Clone
``git clone https://github.com/flslab/FailureHandling.git``

## Set Up Local
Run ``pip3 install -r requirements.txt`` in the root directory. If you are using IDE like PyCharm, you can download all the requirements with it.

## Run Local

The variables specified in ``config.py`` control settings. Once these are adjusted (see below), run:

``python3 primary.py``

After the notification "INFO - Waiting for secondary nodes to connect" shows, run:

`python3 secondary.py`

Need to notice that the result output path is also an adjustable configuration.

## Set Up and Run on Cloud Lab
First, set up a cluster of servers. Creat a cloudlab profile using the file ``profile.py``, then start your own experiments with any chosen type of nodes. 
Ideally, the total number of cores of the servers should equal or be greater than the number of points in the point cloud (number of FLSs).
Otherwise, the lack of cores may cause incorrect results. Normally, when the accessible resource is limited, one core for 2 to 4 points will also work. 
 
After setting up cloudlab, modify the following files based on comment:

* ``gen_conf_cluster``: Identify the path where the gen_conf.py lies
* ``cloudlab_vars.sh``： set the number of nodes 
* ``constants.py``: Set broadcast address and port

Change the configuration for experiments in `gen_conf.py`, this will be the base script to generate configure for each experiment.
Once it's settle, checkout the number of total configurations, and change the number in the For Loop to `the total configuration sets - 1`.
The system will traverse all these configuration sets.

Finally, modify the script `decentralized_gen.sh` following the comment just like previous files. Then run the script to clone the
project and setup on cloudlab (See section above).

Run ``bash setup.sh`` to set up the project.

After all above are done, run `bash nohup_run.sh` on the primary node (node with index 0). Use `tail -f my.log` to trace output in the root directory.

To stop the running process, run the `sudo pkill python3` command in `decentralized_gen.sh`, then run `nohup_kill.sh` on
the primary node.

## Experiment Report

The final report will be generated in a folder named with the experiment configuration, under the result path directory.
A report will include 3 data sheets:
 * Metrics
 * Config
 * Dispatcher

The Metric sheet includes all the reporting information, detailed description shown blown:

| Term                                                    | Definition                                                                                                                                                                                               |
|:--------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| QoI before Reset                                        | Percentage of illuminating FLSs defined as the number of illuminating FLSs divided by the total number of required FLSs (points in a point cloud).  Measured once all initial FLSs have been dispatched. |
| QoI after Reset                                         | Same as above, but measured at the end of the experiment                                                                                                                                                 |
| Dispatched Before Reset                                 | Number of FLSs dispatched before all initial illuminating and initial standby FLSs were dispatched                                                                                                       |
| Dispatched After Reset                                  | Number of FLSs dispatched after all initial illuminating and initial standby FLSs were dispatched                                                                                                        |
| Failure Before Reset                                    | Number of failed FLSs before all initial illuminating and initial standby FLSs were dispatched                                                                                                           |
| Failure After Reset                                     | Number of failed FLSs after all initial illuminating and initial standby FLSs were dispatched                                                                                                            |
| Mid-Flight                                              | Number of mid-flight FLSs at the end of the experiment                                                                                                                                                   |
| Illuminating                                            | Number of illuminating FLSs at the end of the experiment                                                                                                                                                 |
| Stationary Standby                                      | Number of stationary FLSs at the end of the experiment                                                                                                                                                   |
| Avg Travel Time                                         | Depends on the speed model, average time to travel the distance                                                                                                                                          |
| Min Travel Time                                         | Depends on the speed model, min time to travel the distance                                                                                                                                              |
| Max Travel Time                                         | Depends on the speed model, max time to travel the distance                                                                                                                                              |
| Median Travel Time                                      | Depends on the speed model, median time to travel the distance                                                                                                                                           |
| Avg Dist Traveled                                       | Average distance traveled by the dispatched FLSs                                                                                                                                                         |
| Min Dist Traveled                                       | Minimum distance traveled by the dispatched FLSs                                                                                                                                                         |
| Max Dist Traveled                                       | Maximum distance traveled by the dispatched FLSs                                                                                                                                                         |
| Median Dist Traveled                                    | Median distance traveled by the dispatched FLSs                                                                                                                                                          |
| Avg MTTR                                                | Average mean time to repair an FLS                                                                                                                                                                       |
| Min MTTR                                                | Minimum mean time to repair an FLS                                                                                                                                                                       |
| Max MTTR                                                | Maximum mean time to repair an FLS                                                                                                                                                                       |
| Median MTTR                                             | Median mean time to repair an FLS                                                                                                                                                                        |
| Deploy Rate before reset                                | The rate at which a dispatcher deploys FLSs when initiating an illumination                                                                                                                              |
| Deploy rate After Reset                                 | The rate at which a dispatcher deploys FLSs after all FLSs to illuminate a shape have been deployed                                                                                                      |
| Number of Groups                                        | Number of reliability groups                                                                                                                                                                             |
| Min_dist_arrived_illuminate                             | Minimum distance traveled by illuminating FLSs that failed after arrival (distance from dispatcher to illuminating point)                                                                                |
| Max_dist_arrived_illuminate                             | Maximum distance traveled by illuminating FLSs that failed after arrival (distance from dispatcher to illuminating point)                                                                                |
| Avg_dist_arrived_illuminate                             | Average distance traveled by illuminating FLSs that failed after arrival (distance from dispatcher to illuminating point)                                                                                |
| Median_dist_arrived_illuminate                          | Median distance traveled by illuminating FLSs that failed after arrival (distance from dispatcher to illuminating point)                                                                                 |
| Min_dist_failed_midflight_illuminate                    | Minimum distance traveled by illuminating FLSs that failed before arrival (distance from dispatcher to failure point)                                                                                    |
| Max_dist_failed_midflight_illuminate                    | Maximum distance traveled by illuminating FLSs that failed before arrival (distance from dispatcher to failure point)                                                                                    |
| Avg_dist_failed_midflight_illuminate                    | Average distance traveled by illuminating FLSs that failed before arrival (distance from dispatcher to failure point)                                                                                    |
| Median_dist_failed_midflight_illuminate                 | Median distance traveled by illuminating FLSs that failed before arrival  (distance from dispatcher to failure point)                                                                                    |
| Min_dist_stationary_standby_recover_illuminate          | Minimum distance traveled by a stationary standby to successfully recover a failed illuminating FLS                                                                                                      |
| Max_dist_stationary_standby_recover_illuminate          | Maximum distance traveled by a stationary standby to successfully recover a failed illuminating FLS                                                                                                      |
| Avg_dist_stationary_standby_recover_illuminate          | Average distance traveled by a stationary standby to successfully recover a failed illuminating FLS                                                                                                      |
| Median_dist_stationary_standby_recover_illuminate       | Median distance traveled by a stationary standby to successfully recover a failed illuminating FLS                                                                                                       |
| Min_dist_midflight_standby_recover_illuminate           | Minimum distance traveled by a mid-flight standby to successfully recover a failed illuminating FLS                                                                                                      |
| Max_dist_midflight_standby_recover_illuminate           | Maximum distance traveled by a mid-flight standby to successfully recover a failed illuminating FLS                                                                                                      |
| Avg_dist_midflight_standby_recover_illuminate           | Average distance traveled by a mid-flight standby to successfully recover a failed illuminating FLS                                                                                                      |
| Median_dist_midflight_standby_recover_illuminate        | Median distance traveled by a mid-flight standby to successfully recover a failed illuminating FLS                                                                                                       |
| Min_dist_standby_hub_to_centroid                        | Min distance traveled by a standby from dispatcher to its group centroid everytime it successfully complete its trip                                                                                     |
| Max_dist_standby_hub_to_centroid                        | Maximum distance traveled by a standby from dispatcher to its assigned coordinate everytime it successfully complete its trip                                                                            |
| Avg_dist_standby_hub_to_centroid                        | Avg distance traveled by a standby from dispatcher to its assigned coordinate everytime it successfully complete its trip                                                                                |
| Median_dist_standby_hub_to_centroid                     | Median distance traveled by a standby from dispatcher to its assigned coordinate everytime it successfully complete its trip                                                                             |
| Min_dist_standby_hub_to_fail_before_centroid            | Min Distance traveled by a standby FLS that never arrived at its group centroid                                                                                                                          |
| Max_dist_standby_hub_to_fail_before_centroid            | Max Distance traveled by a standby FLS that never arrived at its group centroid                                                                                                                          |
| Avg_dist_standby_hub_to_fail_before_centroid            | Avg Distance traveled by a standby FLS that never arrived at its group centroid                                                                                                                          |
| Median_dist_standby_hub_to_fail_before_centroid         | Median Distance traveled by a standby FLS that never arrived at its group centroid                                                                                                                       |
| Min_dist_standby_centroid_to_fail_before_recovered      | Min distance traveled by a standby stationary FLS that moves from its group centroid to recover a failed illuminating FLS and never arrives at its destination because it fails                          |
| Max_dist_standby_centroid_to_fail_before_recovered      | Max distance traveled by a standby stationary FLS that moves from its group centroid to recover a failed illuminating FLS and never arrives at its destination because it fails                          |
| Avg_dist_standby_centroid_to_fail_before_recovered      | Avg distance traveled by a standby stationary FLS that moves from its group centroid to recover a failed illuminating FLS and never arrives at its destination because it fails                          |
| Median_dist_standby_centroid_to_fail_before_recovered   | Median distance traveled by a standby stationary FLS that moves from its group centroid to recover a failed illuminating FLS and never arrives at its destination because it fails                       |
| Ill_Recovered_By_HUB                                    | Number of failed illuminating FLSs recovered by the Hub dispatching FLSs  (the new FLS arrives at the group centroid)                                                                                    |
| Ill_Recovered_By_Standby                                | Number of failed illuminating FLSs recovered using a standby FLS (the new FLS arrives at the group centroid)                                                                                             |
| Stdby_Recovered_By_Hub                                  | Number of failed standby FLSs recovered by the Hub (the new FLS arrives at the group centroid)                                                                                                           |
| Num_FLSs_Queued                                         | Number of queued FLSs at the end of the experiment                                                                                                                                                       |
| Failed Illuminating FLS                                 | Number of Failed Illuminating FLS                                                                                                                                                                        |
| Failed Standby FLS                                      | Number of Failed Standby FLS After Reset                                                                                                                                                                 |
| Hub_Deployed_FLS                                        | Failures that have been handled by the hub After Reset                                                                                                                                                   |
| Hub_Deployed_FLS_To_Illuminate                          | Number of failed illuminating FLS that have been handled by the hub                                                                                                                                      |
| Hub_Deployed_FLS_For_Standby                            | Number of Failed standby FLS that have been handled by the hub                                                                                                                                           |

The Dispatcher sheet includes all information gathered by the primary node. 
In a Dronevision/FLS Display context, this should be the information from the orchestrator.

| Term             | Definition                                                                                  |
|:-----------------|:--------------------------------------------------------------------------------------------|
| dispatcher_coord | Array of coordinates of each dispatcher                                                     |
| num_dispatched   | Number of FLSs that has been deployed by every dispatcher                                   |
| avg_delay        | Array of Average delay for FLSs dispatched by each dispatcher After initial FLSs dispatched |
| min_delay        | Array of Min delay for FLSs dispatched by each dispatcher After initial FLSs dispatched     |
| max_delay        | Array of Max delay for FLSs dispatched by each dispatcher After initial FLSs dispatched     |
| delay_info       | Lists of delayed time for FLSs dispatched by each dispatcher After initial FLSs dispatched  |
| min_delay        | Overall Min delay for FLSs dispatched by each dispatcher After initial FLSs dispatched      |
| max_delay        | Overall max delay for FLSs dispatched by each dispatcher After initial FLSs dispatched      |
| avg_delay        | Overall average delay for FLSs dispatched by each dispatcher After initial FLSs dispatched  |

## Analytical Models
The movement of FLSs are calculated using the velocity model. We suppose all FLSs have the same maximum speed, maximum acceleration and deceleration.
An FLS's moving time and MTID (Mean time to illuminate a dark point due to FLS failure) is calculated using this model.

Once a reliability group is constructed, there will be a group centroid for standby FLS. The average distance from a group centroid 
to a group member is calculated using the average value of distances of all points to their group centroid.
The Average MTID reported were calculated using the average value of the time for a standby FLS/newly deployed FLS to recover a failed illuminating FLS.
Each of these time is the time traveled for an FLS to arrive at the illuminating point.

The Script to compare two group formation techniques: CANF and k-means can be found in `./util/cmp_shape.py`.
By specifying variables: `shapes, max_speed, max_acceleration, max_deceleration, disp_cell_size`, the report will be generated in `./assets/mtid_report.csv`.

| Term                     | Definition                                                                                                                    |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| Shape                    | Shape that is comparing with.                                                                                                 |
| Method                   | Group formation techniques used.                                                                                              |
| Group Size               | The targeting group size.                                                                                                     |
| Avg Pairwise Distance    | Average distance between points in a group.                                                                                   |
| Avg Centroid Distance    | Average distance from points in each group to their corresponding group centroid.                                             |
| Min GroupSize            | Minimum group size among all group formed. The final group size may be different from the targeting group size.               |
| Median GroupSize         | Median group size among all group formed.                                                                                     |
| Max GroupSize            | Maximum group size among all group formed.                                                                                    |
| Avg MTTR                 | Average value of time need to repair a failed illuminating FLS with its assigned standby FLS (waiting at the group centroid). |
| Min MTTR                 | Minimum value of time need to repair a failed illuminating FLS with its assigned standby FLS (waiting at the group centroid). |
| Median MTTR              | Median value of time need to repair a failed illuminating FLS with its assigned standby FLS (waiting at the group centroid).  |
| Max MTTR                 | Maximum value of time need to repair a failed illuminating FLS with its assigned standby FLS (waiting at the group centroid). |
| Min MTID                 | The time for the group that has the minimum average value for its member points to get recover by it standby FLS.             |
| Median MTID              | The time for the group that has the median average value for its member points to get recover by it standby FLS.              |
| Max MTID                 | The time for the group that has the maximum average value for its member points to get recover by it standby FLS.             |
| Avg Dist To Centroid     | Average distance from each point to its group centroid.                                                                       |
| Min Dist To Centroid     | Minimum distance from each point to its group centroid.                                                                       |
| Median  Dist To Centroid | Median distance from each point to its group centroid.                                                                        |
| Max Dist To Centroid     | Maximum distance from each point to its group centroid.                                                                       |

