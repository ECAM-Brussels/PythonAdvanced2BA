// utils.c
// author: Sébastien Combéfis
// version: April 6, 2016

int cfact (int n)
{
	int result = 1;
	int i;
	for (i = 1; i <= n; i++)
	{
		result *= i;
	}
	return result;
}

int csum (int a, int b)
{
	return a + b;
}