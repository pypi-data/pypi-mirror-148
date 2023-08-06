import numpy as np
from .diagnosis import get_AICc, get_AIC, get_BIC, get_CV
# from scipy.spatial.distance import pdist
from .model import GTWR
from .search import two_d_golden_section, multi_bws

get_diagnosis = {'AICc': get_AICc, 'AIC': get_AIC, 'BIC': get_BIC, 'CV': get_CV}


class SelBws:

    def __init__(
            self,
            coords: np.ndarray,
            t: np.ndarray,
            X: np.ndarray,
            y: np.ndarray,
            kernel: str = 'bisquare',
            fixed: bool = True,
            multi: bool = False,
            constant: bool = True
    ):
        """
        Select bandwidth for kernel

        Parameters
        ----------
        coords        : array-like
                        n*2, collection of n sets of (x,y) coordinates of
                        observatons

        t             : array
                        n*1, time location

        y             : array
                        n*1, dependent variable

        X             : array
                        n*k, independent variable, excluding the constant

        kernel        : string
                        type of kernel function used to weight observations;
                        available options:
                        'gaussian'
                        'bisquare'
                        'exponential'

        fixed         : boolean
                        True for distance based kernel function and  False for
                        adaptive (nearest neighbor) kernel function (default)

        constant      : boolean
                        True to include intercept (default) in model and False to exclude
                        intercept.

        multi          : True for multiple (covaraite-specific) bandwidths
                         False for a traditional (same for  all covariates)
                         bandwidth; default is False.

        Examples
        --------
        import numpy as np
        from mgtwr.sel import SelBws
        from mgtwr.model import GTWR, MGTWR
        np.random.seed(1)
        u = np.array([(i-1)%12 for i in range(1,1729)]).reshape(-1,1)
        v = np.array([((i-1)%144)//12 for i in range(1,1729)]).reshape(-1,1)
        t = np.array([(i-1)//144 for i in range(1,1729)]).reshape(-1,1)
        x1 = np.random.uniform(0,1,(1728,1))
        x2 = np.random.uniform(0,1,(1728,1))
        epsilon = np.random.randn(1728,1)
        beta0 = 5
        beta1 = 3 + (u + v + t)/6
        beta2 = 3+((36-(6-u)**2)*(36-(6-v)**2)*(36-(6-t)**2))/128
        y = beta0 + beta1 * x1 + beta2 * x2 + epsilon
        coords = np.hstack([u,v])
        X = np.hstack([x1,x2])
        sel = SelBws(coords, t, X, y, kernel = 'gaussian', fixed = True)
        bw, tau = sel.search(bw_max = 40, tau_max = 5, verbose = True)
        0.8, 1.1
        """
        self.coords = coords
        self.t = t
        self.n = X.shape[0]
        if constant:
            self.X = np.hstack([np.ones((self.n, 1)), X])
        else:
            self.X = X
        self.k = self.X.shape[1]
        self.y = y
        self.constant = constant
        self.kernel = kernel
        self.fixed = fixed
        self.multi = multi
        self.int_score = not self.fixed
        self.criterion = None
        self.bws = None
        self.tol = None
        self.bw_decimal = None
        self.tau_decimal = None

    def search(
            self,
            criterion: str = 'AICc',
            bw_min: float = None,
            bw_max: float = None,
            tau_min: float = None,
            tau_max: float = None,
            tol: float = 1.0e-6,
            bw_decimal: int = 1,
            tau_decimal: int = 1,
            init_bw: float = None,
            init_tau: float = None,
            multi_bw_min: list = None,
            multi_bw_max: list = None,
            multi_tau_min: list = None,
            multi_tau_max: list = None,
            tol_multi: float = 1.0e-5,
            verbose: bool = False,
            rss_score: bool = False
    ):
        """
        Method to select one unique bandwidth and Spatio-temporal scale for a gtwr model or a
        bandwidth vector and Spatio-temporal scale vector for a mtgwr model.

        Parameters
        ----------
        criterion      : string
                         bw selection criterion: 'AICc', 'AIC', 'BIC', 'CV'
        bw_min         : float
                         min value used in bandwidth search
        bw_max         : float
                         max value used in bandwidth search
        tau_min        : float
                         min value used in spatio-temporal scale search
        tau_max        : float
                         max value used in spatio-temporal scale search
        multi_bw_min   : list
                         min values used for each covariate in mgwr bandwidth search.
                         Must be either a single value or have one value for
                         each covariate including the intercept
        multi_bw_max   : list
                         max values used for each covariate in mgwr bandwidth
                         search. Must be either a single value or have one value
                         for each covariate including the intercept
        multi_tau_min  : list
                         min values used for each covariate in mgtwr spatio-temporal scale
                         search. Must be either a single value or have one value
                         for each covariate including the intercept
        multi_tau_max  : max values used for each covariate in mgtwr spatio-temporal scale
                         search. Must be either a single value or have one value
                         for each covariate including the intercept
        tol            : float
                         tolerance used to determine convergence
        bw_decimal     : int
                        The number of bw decimal places reserved
        tau_decimal    : int
                        The number of tau decimal places reserved
        init_bw        : float
                         None (default) to initialize MGTWR with a bandwidth
                         derived from GTWR. Otherwise this option will choose the
                         bandwidth to initialize MGWR with.
        init_tau       : float
                         None (default) to initialize MGTWR with a spatio-temporal scale
                         derived from GTWR. Otherwise this option will choose the
                         spatio-temporal scale to initialize MGWR with.
        tol_multi      : convergence tolerance for the multiple bandwidth
                         back fitting algorithm; a larger tolerance may stop the
                         algorithm faster though it may result in a less optimal
                         model
        rss_score      : True to use the residual sum of squares to evaluate
                         each iteration of the multiple bandwidth back fitting
                         routine and False to use a smooth function; default is
                         False
        verbose        : Boolean
                         If true, bandwidth searching history is printed out; default is False.
        """
        self.criterion = criterion
        self.tol = tol
        self.bw_decimal = bw_decimal
        self.tau_decimal = tau_decimal
        if self.multi:
            if multi_bw_min is not None:
                if len(multi_bw_min) == self.k:
                    multi_bw_min = multi_bw_min
                elif len(multi_bw_min) == 1:
                    multi_bw_min = multi_bw_min * self.k
                else:
                    raise AttributeError(
                        "multi_bw_min must be either a list containing"
                        " a single entry or a list containing an entry for each of k"
                        " covariates including the intercept")
            else:
                a = self._init_section(bw_min, bw_max, tau_min, tau_max)[0]
                multi_bw_min = [a] * self.k

            if multi_bw_max is not None:
                if len(multi_bw_max) == self.k:
                    multi_bw_max = multi_bw_max
                elif len(multi_bw_max) == 1:
                    multi_bw_max = multi_bw_max * self.k
                else:
                    raise AttributeError(
                        "multi_bw_max must be either a list containing"
                        " a single entry or a list containing an entry for each of k"
                        " covariates including the intercept")
            else:
                c = self._init_section(bw_min, bw_max, tau_min, tau_max)[1]
                multi_bw_max = [c] * self.k

            if multi_tau_min is not None:
                if len(multi_tau_min) == self.k:
                    multi_tau_min = multi_tau_min
                elif len(multi_tau_min) == 1:
                    multi_tau_min = multi_tau_min * self.k
                else:
                    raise AttributeError(
                        "multi_tau_min must be either a list containing"
                        " a single entry or a list containing an entry for each of k"
                        " variates including the intercept")
            else:
                A = self._init_section(bw_min, bw_max, tau_min, tau_max)[2]
                multi_tau_min = [A] * self.k

            if multi_tau_max is not None:
                if len(multi_tau_max) == self.k:
                    multi_tau_max = multi_tau_max
                elif len(multi_tau_max) == 1:
                    multi_tau_max = multi_tau_max * self.k
                else:
                    raise AttributeError(
                        "multi_tau_max must be either a list containing"
                        " a single entry or a list containing an entry for each of k"
                        " variates including the intercept")
            else:
                C = self._init_section(bw_min, bw_max, tau_min, tau_max)[3]
                multi_tau_max = [C] * self.k

        if self.multi:
            self.bws = multi_bws(init_bw, init_tau, self.X, self.y, self.n, self.k, tol_multi,
                                 rss_score, self.gtwr_func, self.bw_func, self.sel_func, multi_bw_min, multi_bw_max,
                                 multi_tau_min, multi_tau_max, verbose=verbose)
            bw = self.bws[0]
            tau = self.bws[1]
            return bw, tau
        else:
            bw, tau = self._bw(bw_min, bw_max, tau_min, tau_max, tol, bw_decimal, tau_decimal, verbose)
            return bw, tau

    def _bw(self, bw_min, bw_max, tau_min, tau_max, tol, bw_decimal, tau_decimal, verbose):
        bw_min, bw_max, tau_min, tau_max = self._init_section(bw_min, bw_max, tau_min, tau_max)
        delta = 0.38197  # 1 - (np.sqrt(5.0)-1.0)/2.0
        bw, tau = two_d_golden_section(bw_min, bw_max, tau_min, tau_max, delta, self.gwr_func, tol,
                                       bw_decimal, tau_decimal, verbose)
        return bw, tau

    def gwr_func(self, bw, tau):
        return get_diagnosis[self.criterion](GTWR(
            self.coords, self.t, self.X, self.y, bw, tau, kernel=self.kernel,
            fixed=self.fixed, constant=False).cal_aic())

    def gtwr_func(self, X, y, bw, tau):
        return GTWR(self.coords, self.t, X, y, bw, tau, kernel=self.kernel,
                    fixed=self.fixed, constant=False).cal_multi()

    def bw_func(self, X, y):
        selector = SelBws(self.coords, self.t, X, y, kernel=self.kernel, fixed=self.fixed,
                          constant=False)
        return selector

    def sel_func(self, bw_func, bw_min=None, bw_max=None, tau_min=None, tau_max=None):
        return bw_func.search(criterion=self.criterion, bw_min=bw_min, bw_max=bw_max, tau_min=tau_min, tau_max=tau_max,
                              tol=self.tol, bw_decimal=self.bw_decimal, tau_decimal=self.tau_decimal, verbose=False)

    def _init_section(self, bw_min, bw_max, tau_min, tau_max):
        # if len(X) > 0:
        #     n_glob = X.shape[1]
        # else:
        #     n_glob = 0
        # if constant:
        #     n_vars = n_glob + 1
        # else:
        #     n_vars = n_glob
        # n = np.array(coords).shape[0]

        # if self.int_score:
        #     a = 40 + 2 * n_vars
        #     c = n
        # else:
        #     sq_dists = pdist(coords)
        #     a = np.min(sq_dists) / 2.0
        #     c = np.max(sq_dists) * 2.0

        # if self.bw_min is not None:
        #     a = self.bw_min
        # if self.bw_max is not None:
        #     c = self.bw_max

        # if self.tau_min is not None:
        #     A = self.tau_min
        # else:
        #     A = 0
        # if self.tau_max is not None:
        #     C = self.tau_max
        # else:
        #     C = 2
        a = bw_min if bw_min is not None else 0
        if bw_max is not None:
            c = bw_max
        else:
            c = max(np.max(self.coords[:, 0]) - np.min(self.coords[:, 0]),
                    np.max(self.coords[:, 1]) - np.min(self.coords[:, 1]))

        A = tau_min if tau_min is not None else 0
        C = tau_max if tau_max is not None else 4

        return a, c, A, C
