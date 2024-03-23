#include <iostream>
#include <cmath>
#include <string>
#include <cstdint>
#include <fstream>
using namespace std;

int main() {
	int n = 0;
	int e = 0;
	int Temp = 0;
	cout << "Input n: ";
	cin >> n;
	cout << "Input e: ";
	cin >> e;
	int o = n;
	int p = 0,q = 0;
	while (Temp != 140737488355327) {
		
		if (o % 2 == 0) {
			p = 2;
			while (o % 2 == 0) {
				o = o / 2;
			}
		}
		for (int i = 3; i <= sqrt(o); i += 2) {
			while (o % i == 0) {
				p = i;
				o = o / i;
			}
		}
		if (o > 2)
			p = o;
		/* Check and print out the values that can be p or q such that n = pq */
		q = n / p;
		cout << "Largest prime factors of " << n
			<< " are " << p << " and " << q << "\n";
		break;
		Temp += 1;
	}
	int x = (p - 1) * (q - 1);
	int phi = x;
	int c = 0, d = 1;

	if (x == 1)
		d = 0;

	while (e > 1) {
		// q is quotient
		int q = e / x;
		int t = x;
		// Euclid's algo
		x = e % x, e = t;
		t = c;

		// Update y and x
		c = d - q * c;
		d = t;
		cout << "t: " << t << " d: " << d << " e: " << e << " q: " << q << " c: " << c << " x: " << x << "\n";
	}

	// Make d positive
	if (d < 0)
		d += phi;

	cout << "d, the modular multiplicative inverse, is: " << d << "\n";

}
