from prefect.orion.orchestration.core_policy import (
    CacheRetrieval,
    HandleTaskTerminalStateTransitions,
    PreventRunningTasksFromStoppedFlows,
    PreventRedundantTransitions,
    SecureTaskConcurrencySlots,
    CopyScheduledTime,
    WaitForScheduledTime,
    RetryFailedTasks,
    RenameReruns,
    UpdateFlowRunTrackerOnTasks,
    CacheInsertion,
    ReleaseTaskConcurrencySlots,
    BaseOrchestrationPolicy,
    CoreTaskPolicy,
)


class OnionCoreTaskPolicy(BaseOrchestrationPolicy):
    """
    Orchestration rules that run against task-run-state transitions
    in priority order.
    """

    def priority():
        return [
            CacheRetrieval,
            HandleTaskTerminalStateTransitions,
            PreventRunningTasksFromStoppedFlows,
            PreventRedundantTransitions,
            # retrieve cached states even if slots are full
            SecureTaskConcurrencySlots,
            CopyScheduledTime,
            WaitForScheduledTime,
            RetryFailedTasks,
            RenameReruns,
            UpdateFlowRunTrackerOnTasks,
            CacheInsertion,
            ReleaseTaskConcurrencySlots,
        ]


CoreTaskPolicy.priority = OnionCoreTaskPolicy.priority
