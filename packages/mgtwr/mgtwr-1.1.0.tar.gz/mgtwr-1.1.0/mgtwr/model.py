import numpy as np
from scipy import linalg
from .kernels import Kernel
from .obj import CalAicObj, CalMultiObj


def _compute_betas_gwr(y, x, wi):
    """
    compute MLE coefficients using iwls routine

    Methods: p189, Iteratively (Re)weighted Least Squares (IWLS),
    Fotheringham, A. S., Brunsdon, C., & Charlton, M. (2002).
    Geographically weighted regression: the analysis of spatially varying relationships.
    """
    xt = (x * wi).T
    xtx = np.dot(xt, x)
    xtx_inv_xt = linalg.solve(xtx, xt)
    betas = np.dot(xtx_inv_xt, y)
    return betas, xtx_inv_xt


class GTWR:
    """
    Geographically and Temporally Weighted Regression
    """

    def __init__(
            self,
            coords: np.ndarray,
            t: np.ndarray,
            X: np.ndarray,
            y: np.ndarray,
            bw: float,
            tau: float,
            kernel: str = 'bisquare',
            fixed: bool = True,
            constant: bool = True
    ):
        """
        Parameters
        ----------
        coords        : array-like
                        n*2, collection of n sets of (x,y) coordinates of
                        observations

        t             : array
                        n*1, time location

        y             : array
                        n*1, dependent variable

        X             : array
                        n*k, independent variable, excluding the constant

        bw            : scalar
                        bandwidth value consisting of either a distance or N
                        nearest neighbors; user specified or obtained using
                        sel

        tau           : scalar
                        spatio-temporal scale

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

        after call fit() method:
        Attributes
        ----------
        obj.betas           : array
                              n*k, estimated coefficients

        obj.pre             : array
                              n*1, predicted y values

        obj.CCT             : array
                              n*k, scaled variance-covariance matrix

        obj.df_model        : integer
                              model degrees of freedom

        obj.df_reside       : array
                              n*1, residuals of the response

        obj.RSS             : scalar
                              residual sum of squares

        obj.CCT             : array
                              n*k, scaled variance-covariance matrix

        obj.ENP             : scalar
                              effective number of parameters, which depends on
                              obj.sigma2

        obj.tr_S            : float
                              trace of S (hat) matrix

        obj.tr_STS          : float
                              trace of STS matrix

        obj.R2              : float
                              R-squared for the entire model (1- RSS/TSS)

        obj.adj_R2          : float
                              adjusted R-squared for the entire model

        obj.aic             : float
                              Akaike information criterion

        obj.aic_c           : float
                              corrected Akaike information criterion to account
                              to account for model complexity (smaller
                              bandwidths)

        obj.bic             : float
                              Bayesian information criterio

        obj.sigma2          : float
                              sigma squared (residual variance) that has been
                              corrected to account for the ENP

        obj.std_res         : array
                              n*1, standardised residuals

        obj.bse             : array
                              n*k, standard errors of parameters (betas)

        obj.diagonal        : array
                              n*1, leading diagonal of S matrix

        obj.CooksD          : array
                              n*1, Cook's D

        obj.t_values        : array
                              n*k, local t-statistics

        obj.llf             : scalar
                              log-likelihood of the full model; see
                              pysal.contrib.glm.family for damily-sepcific
                              log-likelihoods

        Examples
        --------
        import numpy as np
        from mgtwr.model import GTWR
        np.random.seed(1)
        u = np.array([(i -1)%12 for i in range(1,1729)]).reshape(-1,1)
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
        gtwr = GTWR(coords, t, X, y, 0.8, 1.1, kernel='gaussian', fixed=True)
        gtwr.fit()
        print(gtwr.R2)
        0.9834515760708834
        """
        self.coords = coords
        self.t = t
        self.y = y
        self.n = X.shape[0]
        self.bw = bw
        self.tau = tau
        self.kernel = kernel
        self.fixed = fixed
        self.constant = constant
        if self.constant:
            self.X = np.hstack([np.ones((self.n, 1)), X])
        else:
            self.X = X
        self.k = self.X.shape[1]
        self.bw_s = self.bw
        self.bw_t = np.sqrt(self.bw ** 2 / self.tau)
        self.diagonal = None
        self.pre = None
        self.reside = None
        self.betas = None
        self.tr_S = None
        self.ENP = None
        self.tr_STS = None
        self.TSS = None
        self.RSS = None
        self.sigma2 = None
        self.CCT = None
        self.std_res = None
        self.bse = None
        self.cooksD = None
        self.t_values = None
        self.df_model = None
        self.df_reside = None
        self.R2 = None
        self.adj_R2 = None
        self.llf = None
        self.aic = None
        self.aic_c = None
        self.bic = None

    def fit(self):
        """
        fit GTWR models
        """
        diagonal = np.empty((self.n, 1))
        reside = np.empty((self.n, 1))
        pre = np.empty((self.n, 1))
        betas, CCT = np.empty((self.n, self.k)), np.empty((self.n, self.k))
        tr_STS = 0
        for i in range(self.n):
            diagonal[i] = self._local_fit(i)[0]
            reside[i] = self._local_fit(i)[1]
            pre[i] = self._local_fit(i)[2]
            betas[i] = self._local_fit(i)[3]
            CCT[i] = self._local_fit(i)[4]
            tr_STS += self._local_fit(i)[5]
        self.diagonal = diagonal
        self.reside = reside
        self.pre = pre
        self.betas = betas
        self.ENP = np.sum(diagonal)
        self.tr_S = self.ENP
        self.tr_STS = tr_STS
        self.TSS = np.sum((self.y - np.mean(self.y)) ** 2)
        self.RSS = np.sum(reside ** 2)
        self.sigma2 = self.RSS / (self.n - self.ENP)
        self.CCT = CCT * self.sigma2
        self.std_res = self.reside / (np.sqrt(self.sigma2 * (1.0 - self.diagonal)))
        self.bse = np.sqrt(self.CCT)
        self.cooksD = (self.std_res ** 2 * self.diagonal) / (self.ENP * (1.0 - self.diagonal))
        self.t_values = self.betas / self.bse
        self.df_model = self.n - self.tr_S
        self.df_reside = self.n - 2.0 * self.tr_S + self.tr_STS
        self.R2 = 1 - self.RSS / self.TSS
        self.adj_R2 = 1 - (1 - self.R2) * (self.n - 1) / (self.n - self.ENP - 1)
        self.llf = -np.log(self.RSS) * self.n / \
            2 - (1 + np.log(np.pi / self.n * 2)) * self.n / 2
        self.aic = -2.0 * self.llf + 2.0 * (self.tr_S + 1)
        self.aic_c = self.aic + 2.0 * self.tr_S * (self.tr_S + 1.0) / \
            (self.n - self.tr_S - 1.0)
        self.bic = -2.0 * self.llf + (self.k + 1) * np.log(self.n)

    def _build_wi(self, i, bw, tau):

        try:
            wi = Kernel(i, self.coords, self.t, bw, tau, fixed=self.fixed,
                        function=self.kernel).kernel
        except BaseException:
            raise  # TypeError('Unsupported kernel function  ', kernel)

        return wi

    def _local_fit(self, i, final=True, multi=False):
        wi = self._build_wi(i, self.bw, self.tau).reshape(-1, 1)
        betas, inv_xtx_xt = _compute_betas_gwr(self.y, self.X, wi)
        pre = np.dot(self.X[i], betas)[0]
        reside = self.y[i] - pre
        if multi:
            return betas.reshape(-1), reside
        influx = np.dot(self.X[i], inv_xtx_xt[:, i])
        if not final:
            return reside * reside, influx
        Si = np.dot(self.X[i], inv_xtx_xt).reshape(-1)
        CCT = np.diag(np.dot(inv_xtx_xt, inv_xtx_xt.T)).reshape(-1)
        Si2 = np.sum(Si ** 2)
        return influx, reside, pre, betas.reshape(-1), CCT, Si2

    def cal_aic(self):
        RSS = 0
        tr_S = 0
        aa = 0
        for i in range(self.n):
            err2, hat = self._local_fit(i, final=False)
            aa += err2 / ((1 - hat) ** 2)
            RSS += err2
            tr_S += hat
        llf = -np.log(RSS) * self.n / \
            2 - (1 + np.log(np.pi / self.n * 2)) * self.n / 2
        return CalAicObj(float(RSS), tr_S, float(llf), float(aa), self.n)

    def cal_multi(self):
        reside = np.empty((self.n, 1))
        betas = np.empty((self.n, self.k))
        for i in range(self.n):
            betas[i] = self._local_fit(i, multi=True)[0]
            reside[i] = self._local_fit(i, multi=True)[1]
        return CalMultiObj(betas, reside)


class MGTWR(GTWR):
    """
    Multiscale GTWR estimation and inference.

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

    selector      : sel_bw object
                    valid sel_bw object that has successfully called
                    the "search" method. This parameter passes on
                    information from GAM model estimation including optimal
                    bandwidths.

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
    after call fit() method
    Attributes
    ----------
    obj.betas           : array
                          n*k, estimated coefficients

    obj.pre             : array
                          n*1, predicted y values

    obj.CCT             : array
                          n*k, scaled variance-covariance matrix

    obj.df_model        : integer
                          model degrees of freedom

    obj.df_reside       : array
                          n*1, residuals of the response

    obj.RSS             : scalar
                          residual sum of squares

    obj.CCT             : array
                          n*k, scaled variance-covariance matrix

    obj.ENP             : scalar
                          effective number of parameters, which depends on
                          obj.sigma2

    obj.tr_S            : float
                          trace of S (hat) matrix

    obj.tr_STS          : float
                          trace of STS matrix

    obj.R2              : float
                          R-squared for the entire model (1- RSS/TSS)

    obj.adj_R2          : float
                          adjusted R-squared for the entire model

    obj.aic             : float
                          Akaike information criterion

    obj.aic_c           : float
                          corrected Akaike information criterion to account
                          to account for model complexity (smaller
                          bandwidths)

    obj.bic             : float
                          Bayesian information criterio

    obj.sigma2          : float
                          sigma squared (residual variance) that has been
                          corrected to account for the ENP

    obj.std_res         : array
                          n*1, standardised residuals

    obj.bse             : array
                          n*k, standard errors of parameters (betas)

    obj.t_values        : array
                          n*k, local t-statistics

    obj.llf             : scalar
                          log-likelihood of the full model; see
                          pysal.contrib.glm.family for damily-sepcific
                          log-likelihoods

    Examples
    --------
    import numpy as np
    from mgtwr.sel import SelBws
    from mgtwr.model import MGTWR
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
    sel_multi = SelBws(coords, t, X, y, kernel = 'gaussian', fixed = True, multi = True)
    sel_multi.search(multi_bw_min=[0.1],verbose=True,tol_multi=1.0e-4)
    mgtwr = MGTWR(coords, t, X, y, sel_multi, kernel = 'gaussian', fixed = True)
    mgtwr.fit()
    print(mgtwr.R2)
    0.9968863111153037
    """

    def __init__(
            self,
            coords: np.ndarray,
            t: np.ndarray,
            X: np.ndarray,
            y: np.ndarray,
            selector,
            kernel: str = 'bisquare',
            fixed: bool = False,
            constant: bool = True):
        self.selector = selector
        self.bws = self.selector.bws[0]  # final set of bandwidth
        self.taus = self.selector.bws[1]
        self.bw_ts = np.sqrt(self.bws ** 2 / self.taus)
        self.bws_history = selector.bws[2]  # bws history in back_fitting
        self.taus_history = selector.bws[3]
        self.betas = selector.bws[5]
        bw_init = self.selector.bws[7]  # initialization bandwidth
        tau_init = self.selector.bws[8]
        super().__init__(coords, t, X, y, bw_init, tau_init,
                         kernel=kernel, fixed=fixed, constant=constant)
        self.n_chunks = None
        self.ENP_j = None

    def _chunk_compute(self, chunk_id=0):

        n = self.n
        k = self.k
        n_chunks = self.n_chunks
        chunk_size = int(np.ceil(float(n / n_chunks)))
        ENP_j = np.zeros(self.k)
        CCT = np.zeros((self.n, self.k))

        chunk_index = np.arange(n)[chunk_id * chunk_size:(chunk_id + 1) * chunk_size]
        init_pR = np.zeros((n, len(chunk_index)))
        init_pR[chunk_index, :] = np.eye(len(chunk_index))
        pR = np.zeros((n, len(chunk_index),
                       k))  # partial R: n by chunk_size by k

        for i in range(n):
            wi = self._build_wi(i, self.bw, self.tau).reshape(-1, 1)
            xT = (self.X * wi).T
            P = np.linalg.solve(xT.dot(self.X), xT).dot(init_pR).T
            pR[i, :, :] = P * self.X[i]

        err = init_pR - np.sum(pR, axis=2)  # n by chunk_size

        for iter_i in range(self.bws_history.shape[0]):
            for j in range(k):
                pRj_old = pR[:, :, j] + err
                Xj = self.X[:, j]
                n_chunks_Aj = n_chunks
                chunk_size_Aj = int(np.ceil(float(n / n_chunks_Aj)))
                for chunk_Aj in range(n_chunks_Aj):
                    chunk_index_Aj = np.arange(n)[chunk_Aj * chunk_size_Aj:(
                                                                                   chunk_Aj + 1) * chunk_size_Aj]
                    pAj = np.empty((len(chunk_index_Aj), n))
                    for i in range(len(chunk_index_Aj)):
                        index = chunk_index_Aj[i]
                        wi = self._build_wi(index, self.bws_history[iter_i, j],
                                            self.taus_history[iter_i, j])
                        xw = Xj * wi
                        pAj[i, :] = Xj[index] / np.sum(xw * Xj) * xw
                    pR[chunk_index_Aj, :, j] = pAj.dot(pRj_old)
                err = pRj_old - pR[:, :, j]

        for j in range(k):
            CCT[:, j] += ((pR[:, :, j] / self.X[:, j].reshape(-1, 1)) ** 2).sum(
                axis=1)
        for i in range(len(chunk_index)):
            ENP_j += pR[chunk_index[i], i, :]

        return ENP_j, CCT,

    def fit(self, n_chunks=1):
        """
        Compute MGTWR inference by chunk to reduce memory footprint.
        """
        self.n_chunks = n_chunks
        betas = self.selector.bws[5]
        pre = np.sum(self.X * betas, axis=1).reshape(-1, 1)
        result = map(self._chunk_compute, (range(n_chunks)))
        result_list = list(zip(*result))
        ENP_j = np.sum(np.array(result_list[0]), axis=0)
        CCT = np.sum(np.array(result_list[1]), axis=0)
        self.pre = pre
        self.betas = betas
        self.ENP_j = ENP_j
        self.reside = self.y - self.pre
        self.tr_S = np.sum(self.ENP_j)
        self.ENP = self.tr_S
        self.TSS = np.sum((self.y - np.mean(self.y)) ** 2)
        self.RSS = np.sum(self.reside ** 2)
        self.sigma2 = self.RSS / (self.n - self.tr_S)
        self.CCT = CCT * self.sigma2
        self.bse = np.sqrt(self.CCT)
        self.t_values = self.betas / self.bse
        self.df_model = self.n - self.tr_S
        self.R2 = 1 - self.RSS / self.TSS
        self.adj_R2 = 1 - (1 - self.R2) * (self.n - 1) / (self.n - self.ENP - 1)
        self.llf = -np.log(self.RSS) * self.n / \
            2 - (1 + np.log(np.pi / self.n * 2)) * self.n / 2
        self.aic = -2.0 * self.llf + 2.0 * (self.tr_S + 1)
        self.aic_c = self.aic + 2.0 * self.tr_S * (self.tr_S + 1.0) / \
            (self.n - self.tr_S - 1.0)
        self.bic = -2.0 * self.llf + (self.k + 1) * np.log(self.n)
