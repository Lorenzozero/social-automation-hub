"use client";

import { useState, useEffect } from "react";
import { Play, Pause, XCircle, RefreshCw, Clock, CheckCircle, AlertCircle } from "lucide-react";

interface CeleryTask {
  id: string;
  name: string;
  state: string;
  received: number;
  started?: number;
  succeeded?: number;
  failed?: number;
  retries: number;
  args: string;
  kwargs: string;
  exception?: string;
  traceback?: string;
  worker?: string;
}

export default function JobMonitoringPage() {
  const [tasks, setTasks] = useState<CeleryTask[]>([]);
  const [filter, setFilter] = useState<"all" | "active" | "failed" | "succeeded">("all");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTasks();
    const interval = setInterval(fetchTasks, 5000); // Refresh every 5s
    return () => clearInterval(interval);
  }, []);

  const fetchTasks = async () => {
    try {
      // Mock data - replace with real API call
      const mockTasks: CeleryTask[] = [
        {
          id: "task-1",
          name: "core.social.tasks.sync_instagram_metrics",
          state: "PROGRESS",
          received: Date.now() - 30000,
          started: Date.now() - 25000,
          retries: 0,
          args: "['account-123']",
          kwargs: "{}",
          worker: "celery@worker1",
        },
        {
          id: "task-2",
          name: "core.social.tasks.detect_follower_changes",
          state: "SUCCESS",
          received: Date.now() - 60000,
          started: Date.now() - 58000,
          succeeded: Date.now() - 45000,
          retries: 0,
          args: "['account-456']",
          kwargs: "{}",
          worker: "celery@worker1",
        },
        {
          id: "task-3",
          name: "core.posts.tasks.publish_post",
          state: "FAILURE",
          received: Date.now() - 120000,
          started: Date.now() - 118000,
          failed: Date.now() - 100000,
          retries: 2,
          args: "['post-789']",
          kwargs: "{}",
          exception: "APIException: Rate limit exceeded",
          traceback: "Traceback (most recent call last):\n  File...",
          worker: "celery@worker2",
        },
      ];
      setTasks(mockTasks);
      setLoading(false);
    } catch (error) {
      console.error("Failed to fetch tasks:", error);
      setLoading(false);
    }
  };

  const filteredTasks = tasks.filter((task) => {
    if (filter === "all") return true;
    if (filter === "active") return ["PENDING", "STARTED", "PROGRESS", "RETRY"].includes(task.state);
    if (filter === "failed") return task.state === "FAILURE";
    if (filter === "succeeded") return task.state === "SUCCESS";
    return true;
  });

  const getStateIcon = (state: string) => {
    switch (state) {
      case "SUCCESS":
        return <CheckCircle size={20} className="text-success" />;
      case "FAILURE":
        return <XCircle size={20} className="text-error" />;
      case "PROGRESS":
      case "STARTED":
        return <Play size={20} className="text-brand-primary" />;
      case "PENDING":
        return <Clock size={20} className="text-muted" />;
      case "RETRY":
        return <RefreshCw size={20} className="text-warning" />;
      default:
        return <AlertCircle size={20} className="text-muted" />;
    }
  };

  const getStateColor = (state: string) => {
    switch (state) {
      case "SUCCESS":
        return "bg-success-bg text-success";
      case "FAILURE":
        return "bg-error-bg text-error";
      case "PROGRESS":
      case "STARTED":
        return "bg-info-bg text-info";
      case "RETRY":
        return "bg-warning-bg text-warning";
      default:
        return "bg-surface text-muted";
    }
  };

  const formatDuration = (start?: number, end?: number) => {
    if (!start || !end) return "—";
    const duration = end - start;
    return `${(duration / 1000).toFixed(1)}s`;
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <section className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2 bg-gradient-to-r from-brand-primary to-brand-secondary bg-clip-text text-transparent">
            Background Jobs
          </h1>
          <p className="text-sm text-muted">Monitor Celery tasks and queue health</p>
        </div>
        <button onClick={fetchTasks} className="btn-secondary flex items-center gap-2">
          <RefreshCw size={16} />
          Refresh
        </button>
      </section>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="card text-center">
          <p className="text-3xl font-bold text-brand-primary">
            {tasks.filter((t) => ["PENDING", "STARTED", "PROGRESS", "RETRY"].includes(t.state)).length}
          </p>
          <p className="text-sm text-muted mt-1">Active</p>
        </div>
        <div className="card text-center">
          <p className="text-3xl font-bold text-success">
            {tasks.filter((t) => t.state === "SUCCESS").length}
          </p>
          <p className="text-sm text-muted mt-1">Succeeded</p>
        </div>
        <div className="card text-center">
          <p className="text-3xl font-bold text-error">
            {tasks.filter((t) => t.state === "FAILURE").length}
          </p>
          <p className="text-sm text-muted mt-1">Failed</p>
        </div>
        <div className="card text-center">
          <p className="text-3xl font-bold text-foreground">{tasks.length}</p>
          <p className="text-sm text-muted mt-1">Total</p>
        </div>
      </div>

      {/* Filters */}
      <div className="flex gap-2">
        {["all", "active", "failed", "succeeded"].map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f as any)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors capitalize ${
              filter === f
                ? "bg-brand-primary text-white"
                : "bg-surface text-foreground hover:bg-muted"
            }`}
          >
            {f}
          </button>
        ))}
      </div>

      {/* Task List */}
      <div className="space-y-3">
        {loading ? (
          <div className="card text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-4 border-muted border-t-brand-primary mx-auto"></div>
            <p className="text-sm text-muted mt-4">Loading tasks...</p>
          </div>
        ) : filteredTasks.length === 0 ? (
          <div className="card text-center py-12">
            <p className="text-sm text-muted">No tasks found</p>
          </div>
        ) : (
          filteredTasks.map((task) => (
            <details key={task.id} className="card">
              <summary className="flex items-center justify-between cursor-pointer">
                <div className="flex items-center gap-3 flex-1">
                  {getStateIcon(task.state)}
                  <div className="flex-1">
                    <p className="text-sm font-semibold text-foreground">
                      {task.name.split(".").pop()}
                    </p>
                    <p className="text-xs text-muted">
                      {task.worker} · {new Date(task.received).toLocaleTimeString()}
                    </p>
                  </div>
                  <div className="flex items-center gap-3">
                    {task.retries > 0 && (
                      <span className="text-xs bg-warning-bg text-warning px-2 py-1 rounded-full">
                        {task.retries} retries
                      </span>
                    )}
                    <span
                      className={`text-xs px-3 py-1 rounded-full font-medium ${
                        getStateColor(task.state)
                      }`}
                    >
                      {task.state}
                    </span>
                  </div>
                </div>
              </summary>
              <div className="mt-4 pt-4 border-t border-muted space-y-3">
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-xs text-muted mb-1">Task ID</p>
                    <p className="text-xs font-mono bg-surface px-2 py-1 rounded">{task.id}</p>
                  </div>
                  <div>
                    <p className="text-xs text-muted mb-1">Duration</p>
                    <p className="text-xs font-mono bg-surface px-2 py-1 rounded">
                      {formatDuration(
                        task.started,
                        task.succeeded || task.failed || Date.now()
                      )}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-muted mb-1">Args</p>
                    <p className="text-xs font-mono bg-surface px-2 py-1 rounded">{task.args}</p>
                  </div>
                  <div>
                    <p className="text-xs text-muted mb-1">Kwargs</p>
                    <p className="text-xs font-mono bg-surface px-2 py-1 rounded">{task.kwargs}</p>
                  </div>
                </div>
                {task.exception && (
                  <div>
                    <p className="text-xs text-muted mb-1">Exception</p>
                    <pre className="text-xs bg-error-bg text-error p-3 rounded overflow-auto max-h-40">
                      {task.exception}
                    </pre>
                  </div>
                )}
                {task.state === "FAILURE" && (
                  <button className="btn-primary text-xs">Retry Task</button>
                )}
              </div>
            </details>
          ))
        )}
      </div>
    </div>
  );
}
