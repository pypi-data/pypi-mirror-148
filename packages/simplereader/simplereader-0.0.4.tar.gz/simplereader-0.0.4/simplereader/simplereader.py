import csv

###READ###

#Reads file (.txt/.csv) and stores as list of dictionaries
#Format: {'header1': ..., 'header2': ..., ....}
def readTable(file, cols_separated_by=","):
    #store as dictionary: {'header': ...., 'header2': ...., ...}
    #store as [ [....], [....], .... ]
    with open(file, "r", encoding="unicode_escape") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=cols_separated_by)

        data_table = []
        for row in csvreader:
            data_table.append(row)

        #list of dictionaries [ {'Pays': ..., 'Consommation': ..., 'Nobels': ...}, {'Pays': ..., 'Consommation': ..., ..} ]
        table = [dict(zip(data_table[0], data)) for data in data_table[1:]]

    return table

#Print the table as a readable table
def printTable(table):

    #Headers
    headers = list(table[0].keys())

    #Add new line
    #'\t'.join(...) --> join all the words with '\t' in between + '\n' at the end
    string_table = '\t'.join(headers) + '\n'

    #Add rows and tabulations
    for row in table:
        string_table += '\t'.join(row[head] for head in headers) + '\n'

    return print(string_table)

#Get values of a column
def getColumnValues(data, col_name, convert_to="default"):

    col_values = []

    if convert_to == "default": #string
        for i in data:
            col_values.append(i[col_name])

    if convert_to == "int":
        for i in data:
            col_values.append(int(i[col_name]))

    if convert_to == "float":
        for i in data:
            col_values.append(float(i[col_name]))

    return col_values

def getValuesWithThreshold(data, col_name, condition, threshold):

    met = []

    for row in data:
        if condition == "greater-equal":
            if float(row[col_name]) >= threshold:
                met.append(row)

        elif condition == "greater":
            if float(row[col_name]) > threshold:
                met.append(row)

        elif condition == "equal":
            if float(row[col_name]) == threshold:
                met.append(row)

        elif condition == "smaller-equal":
            if float(row[col_name]) <= threshold:
                met.append(row)

        elif condition == "smaller":
            if float(row[col_name]) < threshold:
                met.append(row)

    return met

###STATS###

def getMean(col):
    return sum(col)/len(col)

def getVariance(col):
    mean = getMean(col)
    #-1 for sample; population = no -1
    var = sum((xi - mean) ** 2 for xi in col) / (len(col)-1)
    return var

def getCovariance(col1, col2):
    mean_col1 = getMean(col1)
    mean_col2 = getMean(col2)

    sub_x = [i - mean_col1 for i in col1]
    sub_y = [i - mean_col2 for i in col2]

    sum_val = sum( [sub_y[i]*sub_x[i] for i in range(len(col1))] )
    denominator = float(len(col1)-1)

    return sum_val/denominator

def getStdDeviation(col):
    var = getVariance(col)
    std = var**(1/2)

    return std

def getPearsonCorrelationCoeff(col1, col2):
    covariance = getCovariance(col1,col2)
    stdCol1 = getStdDeviation(col1)
    stdCol2 = getStdDeviation(col2)

    return covariance/(stdCol1*stdCol2)

def getCorrelation(col1, col2):
    #Based on https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3576830/table/T1/
    #abs(0.9) to abs(1.00) = Extremely correlated
    #abs(0.70) to abs(0.90) = Highly correlated
    #abs(0.50) to abs(0.70) = Moderately correlated
    #abs(0.30) to abs(0.50) = Weakly correlated
    #abs(0.00) to abs(0.30) = Negligible correlation

    coeff = getPearsonCorrelationCoeff(col1, col2)
    coeff = abs(coeff)

    #5 > 1
    if coeff >= 0.9: #Extreme
        return 5
    if 0.7 <= coeff < 0.9: #High
        return 4
    if 0.5 <= coeff < 0.7: #Moderate
        return 3
    if 0.3 <= coeff < 0.5: #Weak
        return 2
    if 0.00 <= coeff <0.3: #Negligible
        return 1
