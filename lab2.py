def mult_2x2_matrix(x,y):
    a,b,c,d = x
    e,f,g,h = y
    return (a*e+b*g, a*f+b*h, c*e+d*g, c*f+d*h)

def fastExp1(x,n,mult=lambda a,b: a*b,one=1):
    match n:
        case 0: return one
        case 1: return x
        case 2: return mult(x,x)
        case 3: return mult(mult(x,x),x)

    ans = fastExp1(mult(x,x),n//2,mult,one)
    return ans if 0 == n%2 else mult(ans,x)

def fastExp2(x,n,mult=lambda a,b: a*b,one=1):
    match n:
        case 0: return one
        case 1: return x
        case 2: return mult(x,x)
        case 3: return mult(mult(x,x),x)

    y = fastExp2(x,n//2,mult,one)
    y = mult(y,y)
    return y if 0 == n%2 else mult(x,y)

def fastExp3(x,n,mult=lambda a,b: a*b,one=1):
    ans = one if n % 2 == 0 else x
    if n < 2: return ans
    xToPowerOf2 = mult(x,x)
    n //= 2 # we do this since we already handled the 1's bit
    while n > 1:
        if 1 == n%2:
            ans = mult(ans,xToPowerOf2)
        xToPowerOf2 = mult(xToPowerOf2, xToPowerOf2)
        n //= 2
    return mult(ans, xToPowerOf2)


def fastExp4(x,n,mult=lambda a,b: a*b,one=1):
    if n == 0: return one
    if n == 1: return x

    stack = []
    temp_n = n
    while temp_n > 0:
        stack.append(temp_n & 1)
        temp_n >>= 1 # n // 2

    ans = one
    while stack:
        bit = stack.pop()
        ans = mult(ans, ans)
        if bit == 1:
            ans = mult(ans, x)
    return ans

def fastExp5(x,bits,mult=lambda a,b: a*b,one=1):
    ans = one

    current_x_power = x

    for bit in bits:
        if bit == 1:
            ans = mult(ans, current_x_power)

        current_x_power = mult(current_x_power, current_x_power)

    return ans


def fastExp6(x, bits, mult=lambda a,b: a*b,one=1):
    if len(bits) < 2:
        return x if len(bits)==1 and bits[0] else one
    ans = one
    for bit in bits:
        ans = mult(ans,ans)
        if bit: ans = mult(ans,x)
    return ans


bits_lsb = [1,1,1,0,1,0,1]
bits_msb = [1,0,1,0,1,1,1]

mat = (1,1,1,0)
identity = (1,0,0,1)

print("Here, 2^10:", fastExp4(2,10))
matrix_87 = fastExp4(mat, 87, mult_2x2_matrix, identity)
print("MATRIX 87TH POWER:", matrix_87)


print(fastExp1(mat,87,mult_2x2_matrix, identity))
print(fastExp4(mat,87,mult_2x2_matrix, identity))
print(fastExp5(mat, bits_lsb,mult_2x2_matrix, identity))
print(fastExp6(mat,bits_msb,mult_2x2_matrix, identity))


