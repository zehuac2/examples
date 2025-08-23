import Darwin

/// Returns a human-friendly thread identifier string for the current thread.
/// On Apple platforms this uses `pthread_mach_thread_np` to return the Mach thread id.
public func getThreadId() -> String {
  #if os(macOS) || os(iOS) || os(tvOS) || os(watchOS)
    let p = pthread_self()
    let machTid = pthread_mach_thread_np(p)
    return String(machTid)
  #else
    // Fallback: stringify the pthread handle
    return String(describing: pthread_self())
  #endif
}
