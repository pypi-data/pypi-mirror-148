import scipy.stats
from scipy.optimize import brentq

# Output result with this object
class Power:
    def __init__(self, grp, num, btw, wit, sig, pwr):
        self.groups = grp
        self.n = num
        self.between_var = btw
        self.within_var = wit
        self.sig_level = sig
        self.power = pwr
    
    def print_data(self):
        print(
        '''Balanced one-way analysis of variance power calculation
                 groups = ''' + str(self.groups) + '''
                      n = ''' + str(self.n) + '''
            between_var = ''' + str(self.between_var) + '''
             within_var = ''' + str(self.within_var) + '''
              sig_level = ''' + str(self.sig_level) + '''
                  power = ''' + str(self.power)
        )

# Function to perform power calculations
def power_anova_test(groups=None, n=None, between_var=None, within_var=None, sig_level=0.05, power=None):
    """ A function to calculate a test's power. Comparable to ```power.anova.test()``` in R.

    Exactly one of the parameters must be passed as None, and that parameter is determined from the others.
    Notice that sig_level has a default of 0.05, so None must be explicitly passed if you want it computed.

    :param groups: number of groups
    :type groups: int
    :param n: number of observations per group
    :type n: int
    :param between_var: between group variance
    :type between_var: float
    :param within_var: within group variance
    :type within_var: float
    :param sig_level: significance level (Type I error probability)
    :type sig_level: float
    :param power: power of test (1 minus Type II error probability)
    :type power: float
    :return: parameter which was passed as None
    :rtype float:
    
    """
    
    # Check for errors
    if sum(x is None for x in [groups, n, between_var, within_var, sig_level, power]) != 1:
        raise Exception("exactly one of 'groups', 'n', 'between_var', 'within_var', 'power', and 'sig_level' must be NoneType")
    if (groups is not None) and (groups < 2):
        raise Exception("number of groups must be at least 2")
        
    # Declare calculate_power function
    def calculate_power(grp, num, btw, wit, sig):
        ncp = (grp - 1) * num * (btw/wit)
        q = scipy.stats.f.ppf(1-sig, dfn=grp-1, dfd=(num-1) * grp)
        
        return scipy.stats.ncf.sf(q, dfn=grp-1, dfd=(num-1) * grp, nc=ncp)
    
    # Calculate the argument with NoneType
    # POWER
    if power is None:
        power = calculate_power(groups, n, between_var, within_var, sig_level)
        
        output = Power(grp=groups, num=n, btw=between_var, wit=within_var, sig=sig_level, pwr=power)
        return output
    
    # GROUPS
    elif groups is None:
        grp_funct = lambda x: calculate_power(x, n, between_var, within_var, sig_level) - power
        groups = brentq(grp_funct, 2, 100)
        
        output = Power(grp=groups, num=n, btw=between_var, wit=within_var, sig=sig_level, pwr=power)
        return output

    # N
    elif n is None:
        n_funct = lambda x: calculate_power(groups, x, between_var, within_var, sig_level) - power
        n = brentq(n_funct, 2, 1e+07)

        output = Power(grp=groups, num=n, btw=between_var, wit=within_var, sig=sig_level, pwr=power)
        return output
    
    # BETWEEN_VAR
    elif between_var is None:
        btw_funct = lambda x: calculate_power(groups, n, x, within_var, sig_level) - power
        between_var = brentq(btw_funct, 1e-07, 1e+07)

        output = Power(grp=groups, num=n, btw=between_var, wit=within_var, sig=sig_level, pwr=power)
        return output
    
    # WITHIN_VAR
    elif within_var is None:
        wv_funct = lambda x: calculate_power(groups, n, between_var, x, sig_level) - power
        within_var = brentq(wv_funct, 1e-07, 1e+07)

        output = Power(grp=groups, num=n, btw=between_var, wit=within_var, sig=sig_level, pwr=power)
        return output
    
    # SIG_LEVEL
    elif sig_level is None:
        sig_funct = lambda x: calculate_power(groups, n, between_var, within_var, x) - power
        sig_level = brentq(sig_funct, 1e-10, 1 - 1e-10)

        output = Power(grp=groups, num=n, btw=between_var, wit=within_var, sig=sig_level, pwr=power)
        return output
    
    else:
        raise Exception("internal error")