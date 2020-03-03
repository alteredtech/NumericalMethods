import math
# ==========================================================================
def get_array(n):
    return [x for x in range(0,n)] # Modify to return a list of n terms from 0 to the non-negative integer n-1
# ==========================================================================
def get_factorial(n):
    return math.factorial(n) # Modify to return the factorial of non-negative integer (n)
# ==========================================================================  
def nth_derivative_of_cos(x,n):
    #dictionary to get the different derivative of cos with a modulus get of n with 4 since 
    diction = {0:math.cos(x),1:-math.sin(x),2:-math.cos(x),3:math.sin(x)}
    return diction.get(n%4) # Modify to return the nth derivative of the cos(x) w.r.t x where n is a non-negative integer
# ==========================================================================  
def nth_term_of_taylor_series_of_cos(x,h,n):
    return (nth_derivative_of_cos(x,n)*((h)**n))/(get_factorial(n)) # Modify to return the nth term of the taylor series of the cosine where n is a non-negative integer
# ==========================================================================  
def taylor_series_expansion_of_cos_to_nterms(x,h,n):
    cos_num = 0
    for i in range(n):
        cos_num += nth_term_of_taylor_series_of_cos(x,h,i)
    return cos_num # Modify to return the sum of the terms from 0 to n of the taylor series of the cos(x) at a distance of h from x
# ==========================================================================
if __name__ == "__main__":
    get_array(4) # should return [0,1,2,3]
    get_factorial(0) # should return 1
    nth_derivative_of_cos(math.pi/2,1) # should be equal to -1
    nth_term_of_taylor_series_of_cos(math.pi/2,0.2,1)
    taylor_series_expansion_of_cos_to_nterms(math.pi/2,0.2,20) # should be pretty close to cos(math.pi/2+0.2) when m is large

