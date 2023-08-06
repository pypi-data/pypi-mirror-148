def sqrt(x):
    z = x
    z_prev = x+1
    while z_prev-z > 0.00000001:
        z_prev = z
        z -= (z*z-x)/(2*z)  # decrement by diff and divide by its derivative to scale the value
    
    if int(z) == z:
        return int(z)
    else:
        return z