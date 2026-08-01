type LogLevel = "debug" | "info" | "warn" | "error";

const LOG_LEVEL_PRIORITY: Record<LogLevel, number> = {
  debug: 10,
  info: 20,
  warn: 30,
  error: 40,
};

const configuredLogLevel = (
  import.meta.env.VITE_LOG_LEVEL ?? "info"
).toLowerCase() as LogLevel;

const shouldLog = (level: LogLevel): boolean => {
  const configuredPriority =
    LOG_LEVEL_PRIORITY[configuredLogLevel] ?? LOG_LEVEL_PRIORITY.info;
  return LOG_LEVEL_PRIORITY[level] >= configuredPriority;
};

export const logger = {
  debug: (...message: unknown[]) => {
    if (shouldLog("debug")) {
      console.debug(...message);
    }
  },
  info: (...message: unknown[]) => {
    if (shouldLog("info")) {
      console.info(...message);
    }
  },
  warn: (...message: unknown[]) => {
    if (shouldLog("warn")) {
      console.warn(...message);
    }
  },
  error: (...message: unknown[]) => {
    if (shouldLog("error")) {
      console.error(...message);
    }
  },
};
