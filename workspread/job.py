class Job:
    def __init__(self, tasks: list):
        self._tasks = tasks
        self.results = [None] * len(tasks)
        self._remaining = list(range(len(tasks)))
        self._pending = []

    @property
    def num_remaining(self) -> int:
        return len(self._remaining)

    @property
    def has_remaining(self) -> bool:
        return self.num_remaining > 0
    
    @property
    def num_pending(self) -> int:
        return len(self._pending)
    
    @property
    def num_done(self) -> int:
        return len(self._tasks) - self.num_remaining - self.num_pending
    
    @property
    def all_done(self) -> bool:
        return self.num_remaining == 0 and self.num_pending == 0

    def get_task(self) -> tuple[int, str]:
        index = self._remaining.pop()
        self._pending.append(index)
        return (index, self._tasks[index])

    def report_result(self, index, result) -> None:
        self.results[index] = result
        self._pending.remove(index)

    def report_fail(self, index) -> None:
        self._pending.remove(index)
        self._remaining.append(index)


class JobCollection:
    def __init__(self) -> None:
        self.jobs: list[Job] = []
        
    def num_remaining(self, job_id: int = None) -> int:
        if job_id is None:
            return sum(job.num_remaining for job in self.jobs)
        else:
            return self.jobs[job_id].num_remaining
    
    def has_remaining(self, job_id: int = None) -> bool:
        if job_id is None:
            return any(job.has_remaining for job in self.jobs)
        else:
            return self.jobs[job_id].has_remaining
    
    def num_pending(self, job_id: int = None) -> int:
        if job_id is None:
            return sum(job.num_pending for job in self.jobs)
        else:
            return self.jobs[job_id].num_pending
    
    def num_done(self, job_id: int = None) -> int:
        if job_id is None:
            return sum(job.num_done for job in self.jobs)
        else:
            return self.jobs[job_id].num_done
        
    def all_done(self, job_id: int = None) -> bool:
        if job_id is None:
            return all(job.all_done for job in self.jobs)
        else:
            return self.jobs[job_id].all_done

    def insert(self, job: list) -> int:
        self.jobs.append(Job(job))
        return len(self.jobs) - 1

    def remove(self, job_id: int) -> None:
        pass

    def get_job(self, job_id: int) -> list:
        return self.jobs[job_id].results

    def get_task(self) -> tuple[int, int, str]:
        for job_id, job in enumerate(self.jobs):
            if job.num_remaining > 0:
                task_id, task = job.get_task()
                return job_id, task_id, task

    def report_result(self, job_id, task_id, result) -> None:
        self.jobs[job_id].report_result(task_id, result)

    def report_fail(self, job_id, task_id) -> None:
        self.jobs[job_id].report_fail(task_id)
