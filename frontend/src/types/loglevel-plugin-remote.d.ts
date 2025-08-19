declare module 'loglevel-plugin-remote' {
  interface RemoteOptions {
    url: string;
    method?: string;
    headers?: Record<string, string>;
    format?: (level: string, name: string, timestamp: string, message: string) => any;
    interval?: number;
    timeout?: number;
    level?: string;
    replaceConsole?: boolean;
    withCredentials?: boolean;
    onUnauthorized?: () => void;
    token?: string;
    enable?: boolean;
  }

  interface RemotePlugin {
    apply(logger: any, options: RemoteOptions): void;
  }

  const remote: RemotePlugin;
  export default remote;
}
