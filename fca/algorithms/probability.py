"""
Created on 12.02.2010

@author: jupp
"""
from math import exp, log


def get_intent_probability(self, B):
        ans = 0
        log_p_B = self.log_subset_probability(B)
        p_B = exp(log_p_B)
        if len(B) == 0:
            p_B = 1
            log_p_B = 0
        
        not_B = set()
        for attr in self.p_m.keys():
            if not attr in B:
                not_B.add(attr)
        for k in range(self.n + 1):
            mult = 0
            mult_is_zero = False
            for attr in not_B:
                try:
                    mult += log(1 - ((self.p_m[attr]) ** k))
                except:
                    mult_is_zero = True
                    break
            if mult_is_zero:
                continue
            try:
                if p_B == 1 and self.n == k:
                    return exp(mult)
                else:
                    t = k * log_p_B + (self.n - k) * log((1 - p_B)) + mult
                    t = exp(t)
                    # print k, t
            except:
                t = 0
            nom = range(self.n - k + 1, self.n + 1)
            den = range(1, k + 1)
            if len(den) != len(nom):
                print "False"
            for i in range(len(nom)):
                t *= nom[i] / float(den[i])
            ans += t
        return ans

def log_subset_probability(self, subset):
    ans = 0
    for attr in subset:
        ans += log(self.p_m[attr])
    return ans