import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

sales_frequency = np.array([4647, 5603, 11218, 12378, 15590, 16148, 17906, 21565, 30503, 338018])
#OCT TOP10 4647, 5603, 11218, 12378, 15590, 16148, 17906, 21565, 30503, 338018
#NOV TOP10 6138, 10140, 13042, 18193, 18433, 19772, 23237, 30274, 40834, 382647

t_statistic, p_value = stats.ttest_1samp(sales_frequency, np.mean(sales_frequency))

alpha = 0.05

null_hypothesis_mean = np.mean(sales_frequency)
null_hypothesis_std = np.std(sales_frequency)
null_hypothesis_dist = stats.norm(loc=null_hypothesis_mean, scale=null_hypothesis_std)

x = np.linspace(np.min(sales_frequency),np.max(sales_frequency), 100)

plt.plot(x, null_hypothesis_dist.pdf(x), label="Null Hypothesis")

plt.xlabel('Sales Frequency')
plt.ylabel('Probability Density')
plt.title('Sales Frequency Distribution - Hypothesis Testing')

plt.legend()

plt.axvline(x=null_hypothesis_mean, color='r', linestyle='--', label='Significance Level')

gap=200

if p_value < alpha:
    result_text = 'Reject H0'
    text_y = np.max(null_hypothesis_dist.pdf(x)) * 0.5
    text_x = null_hypothesis_mean - gap
else:
    result_text = 'Fail to Reject H0'
    text_y = np.max(null_hypothesis_dist.pdf(x)) * 0.5
    text_x = null_hypothesis_mean - gap

plt.text(x=text_x, y=text_y, s=result_text, ha='right', va='center', color='red', fontsize=12)
# Show the plot
plt.show()