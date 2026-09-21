'use client';
import { useCallback, useEffect, useRef, useState } from 'react';
import { fetchTaskApi, fetchTasksApi } from '@/lib/api';
import { TaskRunResult } from '@/types';

export function useBackgroundJob(kind: string, onComplete: () => void, enabled = true) {
  const [job, setJob] = useState<TaskRunResult | null>(null);
  const [error, setError] = useState('');
  const callback = useRef(onComplete);
  callback.current = onComplete;
  useEffect(() => {
    if (!enabled) return;
    let cancelled = false;
    fetchTasksApi(kind).then(jobs => { if (!cancelled) setJob(jobs[0] || null); })
      .catch(e => { if (!cancelled) setError(String(e.message)); });
    return () => { cancelled = true; };
  }, [kind, enabled]);
  const taskId = job?.taskId;
  const taskStatus = job?.status;
  useEffect(() => {
    if (!taskId || taskStatus !== 'RUNNING') return;
    const activeTaskId = taskId;
    let cancelled = false;
    let timer: ReturnType<typeof setTimeout>;
    async function poll() {
      try {
        const next = await fetchTaskApi(activeTaskId);
        if (cancelled) return;
        setError('');
        setJob(next);
        if (next.status !== 'RUNNING') { callback.current(); return; }
      } catch (e) {
        if (!cancelled) setError(e instanceof Error ? e.message : 'Mất kết nối theo dõi tác vụ');
      }
      if (!cancelled) timer = setTimeout(poll, 2000);
    }
    timer = setTimeout(poll, 1000);
    return () => { cancelled = true; clearTimeout(timer); };
  }, [taskId, taskStatus]);
  const begin = useCallback((value: TaskRunResult) => { setError(''); setJob(value); }, []);
  return {job, begin, error, running: job?.status === 'RUNNING'};
}

export default function JobStatus({job, error}: {job: TaskRunResult | null; error?: string}) {
  if (!job && !error) return null;
  return <div aria-live="polite" className="p-4 rounded-xl border border-border-subtle bg-canvas space-y-2 text-sm">
    {error && <p role="alert" className="text-rose-700">{error}</p>}
    {job && <>
      <p className={job.status === 'FAILED' ? 'text-rose-700' : job.status === 'PARTIAL' ? 'text-amber-700' : 'text-brand'}>
        <strong>#{job.taskId} · {job.status}</strong> — {job.message}
      </p>
      {job.status === 'RUNNING' && <progress className="w-full" max={100} value={job.progress || 0} />}
      <p className="text-xs text-secondary-text">{job.timestamp} · {job.recordsProcessed || 0} bản ghi</p>
    </>}
  </div>;
}
