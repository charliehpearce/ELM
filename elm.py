"""
Extreme Learning Machine
Essentially a single layer neural net without backprop
https://ieeexplore.ieee.org/document/1380068
"""
import numpy as np

class ELM:
    def __init__(self, hidden_layers = 500) -> None:
        self.hidden_layers = hidden_layers
        
    @staticmethod
    def _relu(x):
        return np.maximum(x,0,x)

    def _init_weights(self, X_size):
        self._input_weights = np.random.normal(size=(X_size,self.hidden_layers))
        self._biases = np.random.normal(size=(self.hidden_layers))

    def _forward(self, X):
        G = np.dot(X, self._input_weights)
        G += self._biases
        H = self._relu(G)
        return H
    
    def train(self, X, y):
        # Init weights
        self._init_weights(X.shape[1])     
        mpinv = np.linalg.pinv(self._forward(X))
        self._output_weights = np.dot(mpinv, y)

    def predict(self, X):
        out = self._forward(X)
        preds = np.dot(out, self._output_weights)
        return preds

if __name__ == "__main__":
    """
    Example usage (requires sklearn for data)
    Categorical labels need to be encoded.
    Scaling of input variables seems to increase accuracy.
    """
    from sklearn.datasets import load_boston
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import MinMaxScaler
    
    scaler = MinMaxScaler()
    X, y = load_boston(return_X_y = True)
    X_scaled = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.33)

    model = ELM(hidden_layers=10000)
    model.train(X_train,y_train)

    for i,x in enumerate(X_test):
        pred = model.predict(x)
        acc = y_test[i]
        print(pred, acc)