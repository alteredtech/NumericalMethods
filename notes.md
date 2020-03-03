# 01/08
## Taylor series
zero order
$f(x_{i+1})=f(x_i)$

first order
$f(x_{i+1})=f(x_i)+f'(x_i)*(x_{i+1}-x_i)$

higher order
$f(x_{i+1})=f(x_i)+f'(x_i)*(x_{i+1}-x_i)+f''(x_i)*(x_{i+1}-x_i)^2/2!+f'''(x_i)*(x_{i+1}-x_i)^3/3!$


$f(x)=e^x=\sum_{i=0}^{\infty} x_i$

# 01/13
$V=\frac{gm}{c}*(1-e^{\frac{-c}{m}t})$

$0=\frac{gm}{c}*(1-e^{\frac{-c}{m}t})-V$

Bracketing is when you find two numbers with different signs. Bisection method is when you find a number and then cut the number in half if it still has the same sign as before. A better way is linear interpolation. 

# 01/15

no open methods are guarantee to converge but bracket methods will
## simple fixed point iteration 

$f(x) = x^2-2x+3$

$0=x^2-2x+3$

$x= (\frac{x^2+3}{2})$

## newton-raphson

$x_{i+1}=x_i-(\frac{f(x_i)}{f'(x_i)})$

$E_a=f(x_i)$

$E_r=f(x_i)-f(x_{i-1})$

## secant method

$x_{i+1}=x_i-(\frac{f(x_i)*(x_{i-1}-x_i)}{f(x_{i-1})-f(x_i)})$

# 1/17

$f(x,y) = x^2 + xy - 10 = 0$

$g(x,y) = y + 3xy^2 - 57 = 0$

$\Delta{x} = h = x_{i+1} - x_i$


