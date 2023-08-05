import signal
import sys
from typing import List, Tuple


class ScaleneSignals:
    def __init__(self) -> None:
        self.start_profiling_signal = signal.SIGILL
        self.set_timer_signals(True)
        if sys.platform != "win32":
            self.stop_profiling_signal = signal.SIGBUS
            self.memcpy_signal = signal.SIGPROF
            # Malloc and free signals are generated by include/sampleheap.hpp.
            self.malloc_signal = signal.SIGXCPU
            self.free_signal = signal.SIGXFSZ
            # Set these by default to virtual time (changeable with `set_timer_signals`)
            self.cpu_timer_signal = signal.ITIMER_VIRTUAL
            self.cpu_signal = signal.SIGVTALRM
        else:
            self.stop_profiling_signal = signal.SIGTERM
            # TO DO - not yet activated for Windows
            self.memcpy_signal = None
            self.malloc_signal = None
            self.free_signal = None
            self.cpu_signal = signal.SIGBREAK
            self.cpu_timer_signal = None

    def set_timer_signals(self, use_virtual_time: bool) -> None:
        """Set up timer signals for CPU profiling."""
        if sys.platform == "win32":
            self.cpu_signal = signal.SIGBREAK
            self.cpu_timer_signal = None
        else:
            if use_virtual_time:
                self.cpu_timer_signal = signal.ITIMER_VIRTUAL
                self.cpu_signal = signal.SIGVTALRM
            else:
                self.cpu_timer_signal = signal.ITIMER_REAL
                self.cpu_signal = signal.SIGALRM

    def get_timer_signals(self) -> Tuple[int, signal.Signals]:
        return self.cpu_timer_signal, self.cpu_signal

    def get_all_signals(self) -> List[int]:
        return [
            self.start_profiling_signal,
            self.stop_profiling_signal,
            self.memcpy_signal,
            self.malloc_signal,
            self.free_signal,
            self.cpu_signal,
        ]
