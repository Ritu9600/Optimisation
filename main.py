#Bounding Phase Method
import math
import random
import matplotlib.pyplot as plt
import numpy as np

#Objective Functions

def plot_x_versus_iterations(x_array, iterations, ylabel, method_name, c):
    x = x_array
    k = iterations

    x_axis=[]

    for i in range(0, k+1):
        x_axis.append(i)

    y_axis = x[abs(len(x_axis)-len(x)):]

    fig= plt.figure()
    axes=fig.add_subplot(111)

    plt.ylabel(ylabel)
    plt.xlabel("Number of iterations")

    axes.plot(x_axis, y_axis)

    for i in range(0,len(y_axis)):
        plt.plot(x_axis[i], y_axis[i], 'ro')

    plt.show(block=False)
    plt.savefig(f"range_plot_for_{ylabel}_{method_name}_part{c}.png")

def plot_range(a, b, new_a, new_b, c, d, method_name):
    x_axis = []
    y_axis = []

    for i in np.linspace(a,b,1000):
        y = objective_function1(i, d, c)
        x_axis.append(i)
        y_axis.append(y)

    fig= plt.figure()
    axes=fig.add_subplot(111)

    plt.xlabel("x")
    plt.ylabel("f(x)")

    axes.plot(x_axis, y_axis)
    axes.plot([new_a], [objective_function1(new_a, d, c)], 'ro')
    axes.plot([new_b], [objective_function1(new_b, d, c)], 'ro')
    plt.show(block=False)
    plt.savefig(f"range_plot_{method_name}_part{c}.png")

def objective_function1(x, maximize,c):
    if c == 1:
        eqn=(2*x-5)**4-(x**2-1)**3
    elif c== 2:
        eqn = 8 + x**3 - 2*x - 2 * math.exp(x)
    elif c== 3:
        eqn = 4 * x * math.sin(x)
    elif c== 4:
        eqn = 2 * (x-3)**2 + math.exp(0.5 * x**2)
    elif c== 5:
        eqn = x**2 - 10*math.exp(0.1*x)
    elif c== 6:
        eqn = 20*math.sin(x) -15 * x**2
    if maximize == 1:
        return -1*(eqn)
    else:
        return eqn
        
x_array = []
def bounding_phase_method(a,b, k):
    #x0 = float(input("Enter the value of the intial guess in the range a to b: "))
    #x_array.append(x0)

    org_a = a
    org_b = b
    x_array = [random.uniform(a, b)]
    delta = random.uniform(0, 1)
    #delta = float(input("Enter the value of delta: "))
    print(delta)
    #x_array.append(x0)
    maximize = float(input("Maximize/ Minimize:(1/-1): "))
    c = float(input("Enter the function number: (1-6)"))
    func_x_minus_d = objective_function1(x_array[k] - delta, maximize, c)
    func_x = objective_function1(x_array[k], maximize, c)
    func_x_plus_d  = objective_function1(x_array[k] + delta, maximize, c)

    print("************")
    print("Bounding Phase Method")
    
    out = open(f"Bounding_Phase_iterations_part{c}.out", "w") 
    
    while True:
        if func_x_minus_d >= func_x and func_x >= func_x_plus_d :
            delta = abs(delta)
            break
        elif func_x_minus_d <= func_x and func_x <= func_x_plus_d :
            delta = -1 * abs(delta)
            break
        else :
            x_array = [random.uniform(a, b)]
            delta = random.uniform(10**-9, 10**-15)

        func_x_minus_d = objective_function1(x_array[k] - delta, maximize, c)
        func_x = objective_function1(x_array[k])
        func_x_plus_d  = objective_function1(x_array[k] + delta, maximize, c)

    out.write("#It: "+str(0)+"\t\t"+"x0-delta: " +str(round(x_array[0] - delta,4))+"\t\t"+"x0: " + str(round(x_array[0],4)) +"\t\t"+"x0+delta: " +str(round(x_array[0] + delta,4)) +"\t\t"+"F(x0-delta): " +str(round(func_x_minus_d,4)) +"\t\t"+"F(x0): " +str(round(func_x,4)) +"\t\t"+"F(x0+delta): " +str(round(func_x_plus_d,4)) )
    out.write("\n")  

    x_array.append(x_array[k] + ((2**k) * delta))

    func_x_k_plus_one = objective_function1(x_array[k+1], maximize, c)
    func_x_k = objective_function1(x_array[k], maximize, c)

    out.write("#It \t\t\tx\t\t\tx_p\t\t\tF_N\t\t\tF_Q")
    out.write("\n")
    
    out.write( str(k)+"\t\t\t"+ str(round(x_array[k+1],4))+"\t\t\t"+ str(round(x_array[k],4)) +"\t\t\t"+str(round(func_x_k,4)) +"\t\t\t"+str(round(func_x_k_plus_one,4)) )
    out.write("\n")  

    while(func_x_k_plus_one<=func_x_k):
        k=k+1
        x_array.append(x_array[k] + ((2**k) * delta))
        
        func_x_k = func_x_k_plus_one
        func_x_k_plus_one = objective_function1(x_array[k+1], maximize, c)
        out.write( str(k)+"\t\t\t"+ str(round(x_array[k+1],4))+"\t\t\t"+ str(round(x_array[k],4)) +"\t\t\t"+str(round(func_x_k,4)) +"\t\t\t"+str(round(func_x_k_plus_one,4)) )
        out.write("\n")

    lowerlimit = x_array[k-1]
    upperlimit = x_array[k+1]
    if lowerlimit>upperlimit:
        upperlimit,lowerlimit=lowerlimit,upperlimit
    
    print(f"The final bracketed interval is: [{lowerlimit}, {upperlimit}]")
    
    epsilon = float(input("Enter the value of epsilon:"))
    maximize = float(input("Maximize/ Minimize: (1/-1): "))

    plot_x_versus_iterations(x_array, k, "X", "bounding_phase_method", c)
    plot_range(org_a, org_b, a, b, c, maximize, "bounding_phase_method")

    secant_method(lowerlimit, upperlimit, epsilon, maximize, c)
    
def differentiate(x1, eta, maximize, c):
    return (objective_function1(x1 + eta, maximize, c) - objective_function1(x1- eta, maximize, c))/(2*eta)
    
def calculate_z(x1, x2, dx1, dx2):
    return (x2 - (dx2/ ((dx2 - dx1)/ (x2 - x1))))
    
def secant_method(a, b, eta, maximize, c):
    #secant_method
    #Step1
    x1 = a
    x2 = b
    dx1 = differentiate(x1, eta, maximize, c)
    dx2 = differentiate(x2, eta, maximize, c)
    func_evaluations = 0
    k = 1 # No. of iterations
    func_evaluations = func_evaluations + 4
    condition = True
    x1_array = [x1]
    x2_array = [x2]

    print("************")
    print("Secant Method")
    out = open(f"secant_search_iterations_part{c}.out", "w") 
    out.write( "a: "+ str(round(a,4))+"\t\t"+ "b: "+str(round(b,4)) +"\t\t"+"dx1: "+str(round(dx1,4)) +"\t\t"+"dx2: "+str(round(dx2,4)))
    out.write("\n")

    out.write("#It \t\tx1\t\tx2\t\tdx1\t\tdx2\t\tz\t\tdz")
    out.write("\n")
    
    while(condition == True):
        #Step 2
        z = calculate_z(x1, x2, dx1, dx2)
        dz = differentiate(z, eta,maximize, c)
        func_evaluations = func_evaluations + 2
        #Step 3
        if(abs(dz) < eta):
            break
        elif(dz < 0):
            if(maximize == -1):
                x1 = z
                dx1 = dz
            elif(maximize == 1):
                x2 = z
                dx2 = dz
            
        elif(dz > 0):
            if(maximize == -1):
                x2 = z
                dx2 = dz
            elif(maximize == 1):
                x1 = z
                dx1 = dz
        
        k = k + 1
        x1_array.append(x1)
        x2_array.append(x2)

        out.write( str(k)+"\t\t"+ str(round(x1,4))+"\t\t"+ str(round(x2,4)) +"\t\t"+str(round(dx1,4)) +"\t\t"+str(round(dx2,4)) +"\t\t"+str(round(z,4)) +"\t\t"+str(round(dz,4)))
        out.write("\n")


    t1=x1
    t2=x2
    if t1>t2:
        t1,t2=t2,t1

    plot_x_versus_iterations(x1_array, k-1, "X_1", "secant_method", c)
    plot_x_versus_iterations(x2_array, k-1, "X_2", "secant_method",c)
    plot_range(a, b, x1, x2, c, maximize, "secant_method")
    
    print(f"The final bracketed interval is: [{t1}, {t2}]")
    print(f"The total number of function evaluations is: {func_evaluations}")
    
#Bounding Phase Method
#Step 1: Choose Initial guess X0 and an increment delta, set k = 0 (k == no. of iterations)
def main():
    
    #x0 = float(input("Enter the value of the initial guess(x0)(from a to b): "))
    #print(x0)
    #delta = float(input("Enter the value of the increment (0 to 1): "))
    #print(delta)
    #maximize = int(input("Maximize/Minimize: (1/0)"))
    k = 0
    a = float(input("Enter the value of a: "))
    b = float(input("Enter the value of b: "))
    
    bounding_phase_method(a, b, k)
    plt.show()
    
main()
