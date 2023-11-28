import scipy.stats as stats
import numpy as np

sales_frequency = np.array([4647, 5603, 11218, 12378, 15590, 16148, 17906, 21565, 30503, 338018])

#OCT TOP10 4647, 5603, 11218, 12378, 15590, 16148, 17906, 21565, 30503, 338018
#NOV TOP10 6138, 10140, 13042, 18193, 18433, 19772, 23237, 30274, 40834, 382647


t_statistic, p_value = stats.ttest_1samp(sales_frequency, np.mean(sales_frequency))

alpha = 3.0
44

if p_value < alpha:
    print("Reject the null hypothesis. There is a significant difference in sales of the top 10 product categories.")

else:
    print("Fail to reject the null hypothesis. There is no significant difference in sales of the top 10 product categories.")