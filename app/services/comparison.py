
def compare_products(products):
    if len(products) < 2:
        return "I need two assessments to compare."

    p1, p2 = products[0], products[1]

    return f'''
{p1['name']} focuses on:
{p1['description']}

Whereas {p2['name']} focuses on:
{p2['description']}
'''
