
# coding: utf-8

# # Capstone Project 1: MuscleHub AB Test

# ## Step 1: Get started with SQL

# Like most businesses, Janet keeps her data in a SQL database.  Normally, you'd download the data from her database to a csv file, and then load it into a Jupyter Notebook using Pandas.
# 
# For this project, you'll have to access SQL in a slightly different way.  You'll be using a special Codecademy library that lets you type SQL queries directly into this Jupyter notebook.  You'll have pass each SQL query as an argument to a function called `sql_query`.  Each query will return a Pandas DataFrame.  Here's an example:

# In[1]:


# This import only needs to happen once, at the beginning of the notebook
from codecademySQL import sql_query


# In[2]:


# Here's an example of a query that just displays some data
sql_query('''
SELECT *
FROM visits
LIMIT 5
''')


# In[3]:


# Here's an example where we save the data to a DataFrame
df = sql_query('''
SELECT *
FROM applications
LIMIT 5
''')


# ## Step 2: Get your dataset

# Let's get started!
# 
# Janet of MuscleHub has a SQLite database, which contains several tables that will be helpful to you in this investigation:
# - `visits` contains information about potential gym customers who have visited MuscleHub
# - `fitness_tests` contains information about potential customers in "Group A", who were given a fitness test
# - `applications` contains information about any potential customers (both "Group A" and "Group B") who filled out an application.  Not everyone in `visits` will have filled out an application.
# - `purchases` contains information about customers who purchased a membership to MuscleHub.
# 
# Use the space below to examine each table.

# In[2]:


# Examine visits here
from codecademySQL import sql_query
sql_query('''
select * from visits limit 5
''')
# The column names of 'visits' are index, first_name, last_name, email, gender and visit_date


# In[3]:


# Examine fitness_tests here
sql_query('''
select * from fitness_tests limit 5
''')
# The column names of 'fitness_tests' are index, first_name, last_name, email, gender and fitness_test_date


# In[4]:


# Examine applications here
sql_query ('''
select * from applications limit 5
''')
# The column names of 'applications' are index, first_name, last_name, email, gender and application_date


# In[5]:


# Examine purchases here
sql_query ('''
select * from purchases limit 5
''')
# The column names of purchases are index, first_name, last_name, email, gender and purchase_date


# We'd like to download a giant DataFrame containing all of this data.  You'll need to write a query that does the following things:
# 
# 1. Not all visits in  `visits` occurred during the A/B test.  You'll only want to pull data where `visit_date` is on or after `7-1-17`.
# 
# 2. You'll want to perform a series of `LEFT JOIN` commands to combine the four tables that we care about.  You'll need to perform the joins on `first_name`, `last_name`, and `email`.  Pull the following columns:
# 
# 
# - `visits.first_name`
# - `visits.last_name`
# - `visits.gender`
# - `visits.email`
# - `visits.visit_date`
# - `fitness_tests.fitness_test_date`
# - `applications.application_date`
# - `purchases.purchase_date`
# 
# Save the result of this query to a variable called `df`.
# 
# Hint: your result should have 5004 rows.  Does it?

# In[152]:


df = sql_query ('''
with previous_query as (select * from visits where visit_date >= '7-1-17')
select 
   previous_query.first_name, 
   previous_query.last_name, 
   previous_query.gender, 
   previous_query.email, 
   previous_query.visit_date,
   fitness_tests.fitness_test_date, 
   applications.application_date, 
   purchases.purchase_date 
 from previous_query 
 left join fitness_tests 
 on 
   previous_query.email = fitness_tests.email
 and 
   previous_query.first_name = fitness_tests.first_name 
 and 
   previous_query.last_name= fitness_tests.last_name
 left join applications 
 on 
   previous_query.email = applications.email 
 and
   previous_query.first_name = applications.first_name 
 and 
   previous_query.last_name = applications.last_name
 left join purchases 
 on 
   previous_query.email = purchases.email 
 and 
   previous_query.first_name = purchases.first_name 
 and 
   previous_query.last_name = purchases.last_name''')
print(df.info())
# the data frame created has 5004 rows! It's important to put the date in the where condition in '' otherwise it returns 6006 rows!


# ## Step 3: Investigate the A and B groups

# We have some data to work with! Import the following modules so that we can start doing analysis:
# - `import pandas as pd`
# - `from matplotlib import pyplot as plt`

# In[27]:


import pandas as pd
from matplotlib import pyplot as plt


# We're going to add some columns to `df` to help us with our analysis.
# 
# Start by adding a column called `ab_test_group`.  It should be `A` if `fitness_test_date` is not `None`, and `B` if `fitness_test_date` is `None`.

# In[29]:


df['ab_test_group'] = df.fitness_test_date.apply( lambda x:
                              'A' if pd.notnull(x) else 'B')
print(df.head(5))


# Let's do a quick sanity check that Janet split her visitors such that about half are in A and half are in B.
# 
# Start by using `groupby` to count how many users are in each `ab_test_group`.  Save the results to `ab_counts`.

# In[30]:


ab_count = df.groupby('ab_test_group').first_name.count().reset_index()
print(ab_count)
# There are 2504 users in group A and 2500 in group B, so the groups are roughly even


# We'll want to include this information in our presentation.  Let's create a pie cart using `plt.pie`.  Make sure to include:
# - Use `plt.axis('equal')` so that your pie chart looks nice
# - Add a legend labeling `A` and `B`
# - Use `autopct` to label the percentage of each group
# - Save your figure as `ab_test_pie_chart.png`

# In[150]:


ab_test_values = [2504, 2500]
ab_test_labels = ["A", "B"]
plt.pie(ab_test_values, autopct = '%0.2f%%', labels = ab_test_labels)
plt.axis('equal')
plt.title("Visitor split into group A and group B")
plt.savefig("ab_test_pie_chart.png")
plt.show()


# ## Step 4: Who picks up an application?

# Recall that the sign-up process for MuscleHub has several steps:
# 1. Take a fitness test with a personal trainer (only Group A)
# 2. Fill out an application for the gym
# 3. Send in their payment for their first month's membership
# 
# Let's examine how many people make it to Step 2, filling out an application.
# 
# Start by creating a new column in `df` called `is_application` which is `Application` if `application_date` is not `None` and `No Application`, otherwise.

# In[43]:


df['is_application'] = df.application_date.apply( lambda x:
                                                'Application' if pd.notnull(x) else 'No Application')
print(df.head(5))


# Now, using `groupby`, count how many people from Group A and Group B either do or don't pick up an application.  You'll want to group by `ab_test_group` and `is_application`.  Save this new DataFrame as `app_counts`

# In[46]:


app_counts = df.groupby(['ab_test_group', 'is_application']).first_name.count().reset_index()
print(app_counts)
# 250 people from group A have submitted an application & 2254 haven't - it looks like the fitness test deters some people.
# 325 people from group B have submitted an application & 2175 haven't - while that's a higher proportion of users who've gone on to submit an application, it's not actually a great number - it's not clear that not having the fitness test is what makes a difference/is that much better. 


# We're going to want to calculate the percent of people in each group who complete an application.  It's going to be much easier to do this if we pivot `app_counts` such that:
# - The `index` is `ab_test_group`
# - The `columns` are `is_application`
# Perform this pivot and save it to the variable `app_pivot`.  Remember to call `reset_index()` at the end of the pivot!

# In[49]:


app_pivot = app_counts.pivot(columns = 'is_application', index = 'ab_test_group', values = 'first_name').reset_index()
print(app_pivot)


# Define a new column called `Total`, which is the sum of `Application` and `No Application`.

# In[52]:


total = lambda row: (row['Application'] + row['No Application'])
app_pivot['Total'] = app_pivot.apply(total, axis = 1)
print(app_pivot.head(5))


# Calculate another column called `Percent with Application`, which is equal to `Application` divided by `Total`.

# In[70]:


percent_app = lambda row: (row['Application'] / float(row['Total']))
app_pivot['Percent with Application'] = app_pivot.apply(percent_app, axis = 1)
print(app_pivot.head(5))
# about 9% of group A and 13% of group B submitted an application, so the impression given just by the raw data above is correct.


# It looks like more people from Group B turned in an application.  Why might that be?
# 
# We need to know if this difference is statistically significant.
# 
# Choose a hypothesis tests, import it from `scipy` and perform it.  Be sure to note the p-value.
# Is this result significant?

# In[78]:


# I think the correct hypothesis test is a Chi Square test, which is ideal for A/B tests
from scipy.stats import chi2_contingency
# the contingency table contains number of apps & number of no apps for each group
contingency = [[250,2254],
              [325,2175]]
chi2, pval, dof, expected = chi2_contingency(contingency)
print pval
if (pval < 0.05):
    print "There is a significant difference between the two groups"
else:
    print "There isn't a significant difference between the two groups"
# the p value is less than 0.05 so we can say there is a significant difference between the two groups


# ## Step 4: Who purchases a membership?

# Of those who picked up an application, how many purchased a membership?
# 
# Let's begin by adding a column to `df` called `is_member` which is `Member` if `purchase_date` is not `None`, and `Not Member` otherwise.

# In[79]:


df['is_member'] = df.purchase_date.apply(lambda x:
                                        'Member' if pd.notnull(x) else 'Not Member')
print(df.head(5))


# Now, let's create a DataFrame called `just_apps` the contains only people who picked up an application.

# In[103]:


# first, I define a variable, members, which is True for every row where is_application column is Application:
applied = df['is_application'] == "Application"
# then I select all cases from df where is_application is Application by using this variable:
just_apps = df[applied]
print(just_apps.head(5))


# Great! Now, let's do a `groupby` to find out how many people in `just_apps` are and aren't members from each group.  Follow the same process that we did in Step 4, including pivoting the data.  You should end up with a DataFrame that looks like this:
# 
# |is_member|ab_test_group|Member|Not Member|Total|Percent Purchase|
# |-|-|-|-|-|-|
# |0|A|?|?|?|?|
# |1|B|?|?|?|?|
# 
# Save your final DataFrame as `member_pivot`.

# In[105]:


# grouping just_apps by whether member and in group A or B:
member_counts = just_apps.groupby(['ab_test_group', 'is_member']).first_name.count().reset_index()
# pivoting member_counts so easier to read:
member_pivot = member_counts.pivot(columns = 'is_member', index = 'ab_test_group', values = 'first_name').reset_index()
# adding count of total users to member_pivot:
total_member = lambda row: (row['Member'] + row['Not Member'])
member_pivot['Total'] = member_pivot.apply(total_member, axis = 1)
# adding percentage of member/total group size to member_pivot:
percent_app_member = lambda row: (row['Member'] / float(row['Total']))
member_pivot['Percent Purchase'] = member_pivot.apply(percent_app_member, axis = 1)
print(member_pivot)
# this time it looks like group A has a higher conversion rate, once an application has been picked up, than group B


# It looks like people who took the fitness test were more likely to purchase a membership **if** they picked up an application.  Why might that be?
# 
# Just like before, we need to know if this difference is statistically significant.  Choose a hypothesis tests, import it from `scipy` and perform it.  Be sure to note the p-value.
# Is this result significant?

# In[106]:


#I think, again, the correct hypothesis test is the Chi Square test. It has already been imported from scipy so won't import again.
contingency_member = [[200,50],
              [250,75]]
chi2, pval_member, dof, expected = chi2_contingency(contingency_member)
print pval_member
if (pval_member < 0.05):
    print "There is a significant difference between the two groups"
else:
    print "There isn't a significant difference between the two groups"
# This time the p value is bigger than 0.05 (at c. 0.4325) so there isn't really a significant difference between the two conversion rates.


# Previously, we looked at what percent of people **who picked up applications** purchased memberships.  What we really care about is what percentage of **all visitors** purchased memberships.  Return to `df` and do a `groupby` to find out how many people in `df` are and aren't members from each group.  Follow the same process that we did in Step 4, including pivoting the data.  You should end up with a DataFrame that looks like this:
# 
# |is_member|ab_test_group|Member|Not Member|Total|Percent Purchase|
# |-|-|-|-|-|-|
# |0|A|?|?|?|?|
# |1|B|?|?|?|?|
# 
# Save your final DataFrame as `final_member_pivot`.

# In[108]:


final_member_counts = df.groupby(['ab_test_group', 'is_member']).first_name.count().reset_index()
# pivoting 
final_member_pivot = final_member_counts.pivot(columns = 'is_member', index = 'ab_test_group', values = 'first_name').reset_index()
# adding count of total users:
final_total_member = lambda row: (row['Member'] + row['Not Member'])
final_member_pivot['Total'] = final_member_pivot.apply(final_total_member, axis = 1)
# adding percentage :
final_percent_app_member = lambda row: (row['Member'] / float(row['Total']))
final_member_pivot['Percent Purchase'] = final_member_pivot.apply(final_percent_app_member, axis = 1)
print(final_member_pivot)
# this time the conversion of group B looks significantly better to the naked eye. Let's see...


# Previously, when we only considered people who had **already picked up an application**, we saw that there was no significant difference in membership between Group A and Group B.
# 
# Now, when we consider all people who **visit MuscleHub**, we see that there might be a significant different in memberships between Group A and Group B.  Perform a significance test and check.

# In[109]:


contingency_final_member = [[200,2304],
              [250,2250]]
chi2, pval_final_member, dof, expected = chi2_contingency(contingency_final_member)
print pval_final_member
if (pval_final_member < 0.05):
    print "There is a significant difference between the two groups"
else:
    print "There isn't a significant difference between the two groups"
# As the 'naked eye' first impression suggested, there is a significant difference. The p value is less than 0.05 (at c. 0.01472) so the overall conversion of group B is better. 
# Overall, not having a fitness test is better for getting people to join.


# ## Step 5: Summarize the acquisition funel with a chart

# We'd like to make a bar chart for Janet that shows the difference between Group A (people who were given the fitness test) and Group B (people who were not given the fitness test) at each state of the process:
# - Percent of visitors who apply
# - Percent of applicants who purchase a membership
# - Percent of visitors who purchase a membership
# 
# Create one plot for **each** of the three sets of percentages that you calculated in `app_pivot`, `member_pivot` and `final_member_pivot`.  Each plot should:
# - Label the two bars as `Fitness Test` and `No Fitness Test`
# - Make sure that the y-axis ticks are expressed as percents (i.e., `5%`)
# - Have a title

# In[147]:


# bar chart for applications by test group
groups = ["Fitness Test", "No Fitness Test"]
values = app_pivot["Percent with Application"].values
plt.bar(range(len(app_pivot)),values)
ax = plt.subplot()
ax.get_children()[0].set_color('r')
ax.set_xticks(range(len(app_pivot)))
ax.set_xticklabels(groups)
ax.set_yticks([0, 0.05, 0.10, 0.15])
ax.set_yticklabels(["0%", "5%", "10%", "15%"])
plt.title("Percentage of gym visitors who apply, by test group")
plt.savefig("percentage_who_apply_by_test_group.png")
plt.show()


# In[148]:


# bar chart for purchase of membership after application (application is not null)
groups_member = ["Fitness Test", "No Fitness Test"]
values_member = member_pivot["Percent Purchase"].values
plt.bar(range(len(member_pivot)),values_member)
ax = plt.subplot()
ax.get_children()[0].set_color('r')
ax.set_xticks(range(len(member_pivot)))
ax.set_xticklabels(groups_member)
ax.set_yticks([0, 0.20, 0.40, 0.60, 0.80])
ax.set_yticklabels(["0%", "20%", "40%", "60%", "80%"])
plt.title("Percentage of gym visitors who purchase a membership after applying")
plt.savefig("percentage_member_after_apply.png")
plt.show()


# In[149]:


# bar chart for purchase of membership by test group
groups_final_member = ["Fitness Test", "No Fitness Test"]
values_final_member = final_member_pivot["Percent Purchase"].values
plt.bar(range(len(final_member_pivot)), values_final_member)
ax = plt.subplot()
ax.get_children()[0].set_color('r')
ax.set_xticks(range(len(final_member_pivot)))
ax.set_xticklabels(groups_final_member)
ax.set_yticks([0, 0.05, 0.10, 0.15])
ax.set_yticklabels(["0%", "5%", "10%", "15%"])
plt.title("Percentage of gym visitors who purchase a membership by test group")
plt.savefig('member_by_test_group.png')
plt.show()

