"use client";

import { useState, useCallback, useRef } from "react";
import { useToast } from "./Toast";

interface UseApiOptions {
  onSuccess?: (data: any) => void;
  onError?: (error: Error) => void;
}

export function useApi<T = any>(url: string, options: UseApiOptions = {}) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const toast = useToast();
  const abortControllerRef = useRef<AbortController | null>(null);

  const execute = useCallback(
    async (fetchOptions: RequestInit = {}) => {
      // Cancel previous request if still pending
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }

      abortControllerRef.current = new AbortController();

      setLoading(true);
      setError(null);

      try {
        const response = await fetch(url, {
          ...fetchOptions,
          signal: abortControllerRef.current.signal,
          headers: {
            "Content-Type": "application/json",
            ...fetchOptions.headers,
          },
        });

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(
            errorData.message ||
              errorData.detail ||
              `Request failed with status ${response.status}`
          );
        }

        const result = await response.json();
        setData(result);
        options.onSuccess?.(result);
        return result;
      } catch (err: any) {
        if (err.name === "AbortError") {
          // Request was cancelled, don't show error
          return;
        }

        const error = err instanceof Error ? err : new Error("Unknown error");
        setError(error);
        options.onError?.(error);
        toast.error(error.message);
        throw error;
      } finally {
        setLoading(false);
      }
    },
    [url, options, toast]
  );

  const reset = useCallback(() => {
    setData(null);
    setError(null);
    setLoading(false);
  }, []);

  return { data, loading, error, execute, reset };
}

// Helper for retry logic
export function useApiWithRetry<T = any>(
  url: string,
  maxRetries = 3,
  retryDelay = 1000
) {
  const [retryCount, setRetryCount] = useState(0);
  const api = useApi<T>(url, {
    onError: (error) => {
      if (retryCount < maxRetries) {
        setTimeout(() => {
          setRetryCount((c) => c + 1);
          api.execute();
        }, retryDelay * Math.pow(2, retryCount)); // Exponential backoff
      }
    },
  });

  return { ...api, retryCount };
}
