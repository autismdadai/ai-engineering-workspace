#!/usr/bin/env python3
"""Quantum Entanglement Lab v1.2 — all tests in one file. Requires: pip install qutip

v1.1: teleportation is checked on six message states instead of only |+>, and
every hand-built gate must be unitary. v1.0 could not see bugs in Bob's X fix
(X leaves |+> unchanged) or a Hadamard missing its 1/sqrt(2) (QuTiP's fidelity
of an unnormalized ket can exceed 1).
v1.2: three checks that could not fail now can. Partial measurement also checks
that each outcome leaves |00> or |11> (v1.1 checked only the 50/50 odds, so the
wrong Bell state passed). CHSH must equal 2*sqrt(2), not just exceed 2.8 (an
angle 0.05 rad off passed). The script refuses to run under python -O, which
strips every assert. evals/mutation_check.py tests the tests.
"""
if not __debug__:
    raise SystemExit("Run without python -O: every check in this lab is an assert, and -O removes them.")
import numpy as np
from qutip import *
I,X,Z = qeye(2),sigmax(),sigmaz()
P0=basis(2,0)*basis(2,0).dag(); P1=basis(2,1)*basis(2,1).dag()
H=(X+Z)/np.sqrt(2)
CNOT=tensor(P0,I)+tensor(P1,X)
C01=tensor(P0,I,I)+tensor(P1,X,I)
for G in (H,CNOT,C01):  # hand-built gates must be unitary
    assert (G.dag()*G-qeye(G.dims[0])).norm()<1e-9, "a hand-built gate is not unitary"
def bell(i):
    b00,b11=tensor(basis(2,0),basis(2,0)),tensor(basis(2,1),basis(2,1))
    b01,b10=tensor(basis(2,0),basis(2,1)),tensor(basis(2,1),basis(2,0))
    return [(b00+b11).unit(),(b00-b11).unit(),(b01+b10).unit(),(b01-b10).unit()][i]

phi=bell(0); S=entropy_vn(phi.ptrace(0),base=2)
assert abs(S-1)<1e-6; print(f"[PASS] S(φ+)={S:.6f}")

assert fidelity(tensor(X,I)*phi,bell(2))>0.999
assert fidelity(tensor(Z,I)*phi,bell(1))>0.999
print("[PASS] X/Z local flips")

for m,Pm in ((0,P0),(1,P1)):  # each outcome has probability 1/2 and leaves |mm>
    assert abs(expect(tensor(Pm,I),phi)-0.5)<1e-6
    assert fidelity((tensor(Pm,I)*phi).unit(),tensor(basis(2,m),basis(2,m)))>0.999
print("[PASS] partial Z")

dec=tensor(H,I)*CNOT
maps={0:(0,0),1:(1,0),2:(0,1),3:(1,1)}
for i in range(4):
    assert fidelity(dec*bell(i),tensor(basis(2,maps[i][0]),basis(2,maps[i][1])))>0.999
print("[PASS] Bell decoder")

singlet=bell(3)
def E(ta,tb):
    A=np.cos(ta)*Z+np.sin(ta)*X; B=np.cos(tb)*Z+np.sin(tb)*X
    return expect(tensor(A,B),singlet)
Sval=abs(E(0,np.pi/4)+E(0,-np.pi/4)+E(np.pi/2,np.pi/4)-E(np.pi/2,-np.pi/4))
assert abs(Sval-2*np.sqrt(2))<1e-6; print(f"[PASS] CHSH |S|={Sval:.6f}")

def ket(theta,ph):  # cos(θ/2)|0> + e^{iφ} sin(θ/2)|1>
    return (np.cos(theta/2)*basis(2,0)+np.exp(1j*ph)*np.sin(theta/2)*basis(2,1)).unit()
# |0>,|1> expose Z-type bugs; |+>,|+i> expose X-type bugs; the last two are generic
messages=[ket(0,0),ket(np.pi,0),ket(np.pi/2,0),ket(np.pi/2,np.pi/2),ket(1.1,0.7),ket(2.3,4.1)]
corr={(0,0):I,(0,1):X,(1,0):Z,(1,1):Z*X}
for msg in messages:
  tot=tensor(msg,bell(0))
  dec3=tensor(H,I,I)*C01*tot
  for m0 in [0,1]:
    for m1 in [0,1]:
      Pr=tensor(basis(2,m0)*basis(2,m0).dag(),basis(2,m1)*basis(2,m1).dag(),I)
      bob=(Pr*dec3).unit().ptrace(2)
      U=corr[(m0,m1)]; fid=fidelity(U*bob*U.dag(),ket2dm(msg))
      assert fid>0.999
print("[PASS] teleportation all branches F=1")
print("ALL TESTS PASSED — you have a working entanglement laboratory.")
