from scipy.optimize import minimize

def dp(x,y):
    result = 0
    for i in range(len(x)):
        result += x[i]*y[i]
    return result

def diff(data, regularisation=0, filter=True):
    def func(weights):
        result = 0
        for whole, parts, weight in data:
            if filter and weight < 3.54: # Remove SentiSpin-only entries
                continue
            #parts = list(parts)
            while len(parts) > 1:
                left, right = parts[-2:]
                vector = (left, right, left*right)
                output = dp(weights, vector)
                parts = parts[:-2] + (output,)
            result += (whole - parts[0])**2 *weight
        for w in weights:
            result += regularisation * w**2
        return result
    return func


if __name__ == '__main__':
    import pickle
    with open("../../data/morph/simple_nopos.pk", 'rb') as f:
        data = pickle.load(f)
    
    result = minimize(diff(data), [ 0.34093843,  0.6214385 ,  0.30980961], tol=10**-9, method='L-BFGS-B', options={'disp':True}, callback=print)
    print('weights:', result['x'])


# [ 0.11959419,  0.18485644,  0.05950508] no weighting, no regularisation
# [ 0.14670987,  0.23959953,  0.10608152] with weights, no regularisation
# [ 0.34534428,  0.62060781,  0.27598586] weights, only if > 3.54, no regularisation