#include <iostream>
#include <tuple>        // std::tuple, std::make_tuple, std::tie
using namespace std;

// Recursive function to demonstrate the extended Euclidean algorithm.
// It returns multiple values using tuple in C++.
tuple<int, int, int> extended_gcd(int a, int b)
{
    if (a == 0) {
        cout << "a: " << a << " b: " << b << "\n" << endl;
        return make_tuple(b, 0, 1);
    }

    int gcd, x, y;

    // unpack tuple returned by function into variables
    tie(gcd, x, y) = extended_gcd(b % a, a);
    cout << "y: " << y << " gcd: " << gcd << " b: " << b << " x: " << x << " a: " << a << "\n" << endl;
    return make_tuple(gcd, (y - (b / a) * x), x);
}

int main()
{
    int a = 0;
    int b = 0;
    cout << "Formula: a^(-1) mod b";
    cout << "Input a: ";
    cin >> a;
    cout << "Input b: ";
    cin >> b;
    tuple<int, int, int> t = extended_gcd(a, b);

    int gcd = get<0>(t);
    int x = get<1>(t);
    int y = get<2>(t);

    cout << "y: " << y << " gcd: " << gcd << " b: " << b << " x: " << x << " a: " << a << "\n" << endl;
    cout << "1 = " << a << " * " << x << " + " << b << " * " << y << "\n" << endl;
    cout << "Inverse: " << x << endl;
 

    return 0;
}
