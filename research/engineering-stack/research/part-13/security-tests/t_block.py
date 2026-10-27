import sys, socket
sys.path.insert(0, "/home/claude/part13/phase4/security/lab/engineering-stack-lab-part-13")
import crosscheck          # installs the blocker on import; main() not run
L = socket.socket(); L.bind(("127.0.0.2", 0)); L.listen(); P = L.getsockname()[1]
U = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); U.bind(("127.0.0.2", 0)); UP = U.getsockname()[1]
def tryit(label, fn):
    try: print(f"{label:44} -> {fn()!r}")
    except Exception as e: print(f"{label:44} -> {type(e).__name__}: {e}")
tryit("socket.connect(('127.0.0.2', p))", lambda: socket.socket().connect(("127.0.0.2", P)))
tryit("socket.connect_ex(('127.0.0.2', p))  [0 = connected]", lambda: socket.socket().connect_ex(("127.0.0.2", P)))
tryit("UDP sendto(('127.0.0.2', p))  [bytes sent]", lambda: socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(b"x", ("127.0.0.2", UP)))
tryit("UDP datagram arrived", lambda: U.recvfrom(10)[0])
tryit("socket.getaddrinfo('lab-check.invalid', 80)", lambda: socket.getaddrinfo("lab-check.invalid", 80))
print("blocker's log of outside attempts:", crosscheck._outside)
