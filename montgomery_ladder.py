from sage.all import *


def cswap(bit, R, S):
    """Conditional swap of two points R and S.
    If bit == 1, then swap R and S.
    If bit == 0, then do nothing.
    """
    if bit == 1:
        return S, R
    else:
        return R, S

def montgomery_ladder(k, P, E):
    k = k % E.order() # since P^ord(E) = 1, P^k = P^k.old
    l = ceil(log(E.order(), 2)) #nr of bits needed to represent the power k. 
    A = k.digits(2, padto = l)
    A.reverse() # A is a binary MSB-left representation of k
    P0 = E(0)
    P1 = P
    # Let A = e_0, e_1,..,e_l - 1
    # Invariant: P0 = P^{e_0,..,e_i-1} and P1 - P0 = P. 
    for i in range(0, l , 1):
        # P0 = P^{e_0,..,e_i-1} and P1 - P0 = P. 
        # assume A[i]
        #   assume A[i]
        #   P0 + P1 = P0 + P + P0 = 2*P0 + P = 2 * P^{e_0,..,e_i-1} + P = P^{e_0,..,e_i-1,1} = P^{e_0,..,e_i}
        #   2*P1 - P1 - P0 = P1 - P0 = P0 + P - P0 = P
        #   assume -A[i]
        #   Contradiction 
        # assume -A[i]
        #   assume A[i]
        #   contradiction
        #   assume -A[i]
        #       2*P0 = P^{e_0,..,e_i-1, 0} = P^{e_0,..,e_i-1, e_i}
        #       P0 + P1 - 2*P0 = P1 - P0 = P
        #if A[i], then if A[i], then P1 + P0 = P^{e_0,..,e_i} and 2*P1 - P1 - P0 = P, else 2*P1 = P^{e_0,..,e_i} and P1 + P0 - 2*P1 = P else A
        (P0, P1) = cswap(A[i], P0, P1) 
        # A = if A[i], then P0 + P1 = P^{e_0,..,e_i} and 2*P0 - P0 - P1 = P, else 2*P0 = P^{e_0,..,e_i} and P0 + P1 - 2*P0 = P
        P1 = P0 + P1
        # if A[i], then P1 = P^{e_0,..,e_i} and 2*P0 - P1 = P, else 2*P0 = P^{e_0,..,e_i} and P1 - 2*P0 = P
        P0 = 2*P0
        # if A[i], then P1 = P^{e_0,..,e_i} and P0 - P1 = P, else P0 = P^{e_0,..,e_i} and P1 - P0 = P
        (P0, P1) = cswap(A[i], P0, P1)
        # P0 = P^{e_0,..,e_i} and P1 - P0 = P. 
        # i = i + 1
        # P0 = P^{e_0,..,e_i-1} and P1 - P0 = P. 

    #P0 = P^{e_0,..,e_i-1} = P^A = P^k, where k is the decimal representation of A
    return P0

if __name__== "__main__":
    F = GF(43)
    E = EllipticCurve(F, [0, 0, 0, 1, 3])
    P = E(19, 42)
    print(montgomery_ladder(9, P, E))
    print(9*E(19, 42))