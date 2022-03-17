import numpy as np


class KalmanFilter:

    def __init__(self, initialestimate):
        self.dt = 0.1
        self.x = np.array([[initialestimate], [0]])
        self.P = np.array([[5, 0], [0, 5]])
        self.A = np.array([[1, self.dt], [0, 1]])
        self.H = np.array([[1, 0]])
        self.HT = np.array([[1], [0]])
        self.R = 10
        self.Q = np.array([[1, 0], [0, 3]])

    def filter(self, newestimate):
        x_p = self.A.dot(self.x)
        # Predict Covariance Forward
        P_p = self.A.dot(self.P).dot(self.A.T) + self.Q
        # Compute Kalman Gain
        S = self.H.dot(P_p).dot(self.HT) + self.R
        K = P_p.dot(self.HT) * (1 / S)
        # Estimate State
        residual = newestimate - self.H.dot(x_p)
        self.x = x_p + K * residual
        # Estimate Covariance
        self.P = P_p - K.dot(self.H).dot(P_p)
        lowbound2sigma = self.x[0] - 2 * np.sqrt(self.P[0][0])
        hibound2sigma = self.x[0] + 2 * np.sqrt(self.P[0][0])
        return [self.x[0], self.P, lowbound2sigma, hibound2sigma]  # x[0] : estimated mean, P : covariance
