#! /usr/bin/env python3
# coding=utf-8

"""
* DISCLAIMER:
*
* IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
* ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
* (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
* LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
* ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
* (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
* SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Helper funcions

 Usage:
  $python app.py;

 @author Ioannis K Breier <ioanniskbreier@gmail.com>
 """

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from IPython.core.display import HTML

def hist_box_plot(x, x_label, y_label, bin_incr):
    '''Take an array as input and draw a histogram with a boxblot above it'''
    f, (ax_box, ax_hist) = plt.subplots(2,
                                        sharex=True,
                                        gridspec_kw={
                                            "height_ratios": (.15, .85)},
                                        figsize=(14, 6))

    sns.boxplot(x, ax=ax_box)
    bins = np.arange(0, x.max() + bin_incr, bin_incr)
    x.hist(grid=False, bins=bins)
    ax_box.set(yticks=[])
    ax_hist.set_ylabel(y_label)
    ax_hist.set_xlabel(x_label)
    sns.despine(ax=ax_hist)
    sns.despine(ax=ax_box, left=True)

def get_description(column_name, schema):
    '''Returns decription on column based on data schema
    
    Parameters
    ----------
    column_name : string 
        the desired columnto return description
    schema : pandas.DataFrame
        the dtaframe containing the data schema to be parsed
        
    Returns
    -------
    desc : string
        the description of the column
            
    '''
    return schema[schema.Column == column_name].Question.values[0]

def print_perc_nans(df, col):
    '''Prints percentage of NaNs in a pandas series'''
    
    print(f'Percentage of NaNs in {col}: ',
          round(df[col].isna().mean() * 100, 2),
          '%')
    
def group(df, group_col, val_col):
    '''groupby and return grouped'''
    props = (df.groupby([group_col])[val_col]
                 .value_counts(normalize=True)
                 .rename('percentage')
                 .mul(100) 
                 .reset_index()
                 .sort_values(val_col))
    return props

def group_plot(df, group_col, val_col, prop=True, orient='h', figsize=(14,8)):
    '''group by group col and val_col and plot a barplot'''
    plt.figure(figsize=(14,8))
    props = (df.groupby([group_col])[val_col]
                 .value_counts(normalize=True)
                 .rename('percentage')
                 .mul(100) 
                 .reset_index()
                 .sort_values(val_col))
    
    order=['Data Science Developer', 'Other Developer']
    
    if orient == 'h':
        p = sns.barplot(y=val_col, x='percentage', hue=group_col, hue_order=order,
                        estimator=np.mean, data=props) 
    else:
        p = sns.barplot(x=val_col, y='percentage', hue=group_col,
                        hue_order=order, estimator=np.mean, data=props) 
        
    plt.legend(title='')
    sns.despine(top=True, right=True, left=False, bottom=False);
    
def Groupby_OneCol_comp_plot(df, col, plt_style = 'seaborn-ticks', color_palette = "pastel", title=''):
    '''
    Group by col1, sort by size , return and plot the dataframe with a bar and pie plot
    '''
    opacity=0.85
    gr=pd.DataFrame()
    gr['{} No'.format(col)] = df.groupby(col).size()
    gr['{} Ratio'.format(col)] = np.round(gr['{} No'.format(col)].divide(gr['{} No'.format(col)].sum())*100,0)
    
    print ('Total No. of {}:{}'.format(col,gr['{} No'.format(col)].sum()))
    
    plt.style.use(plt_style)
    sns.set_palette(sns.color_palette(color_palette))
    
    
    fig=plt.figure()
    plt.axis('off')

    fig.add_subplot(121)
    
    ax=gr['{} No'.format(col)].plot(kind='bar', title='{} Counts'.format(title), figsize=(16,8),
                                    color=sns.color_palette(),
                                    alpha=opacity)
    _ = plt.setp(ax.get_xticklabels(), rotation=0)
    for p in ax.patches: ax.annotate(np.round(p.get_height(),decimals=2),
                                     (p.get_x()+p.get_width()/2., p.get_height()),
                                     ha='center', va='center', xytext=(0, 10), textcoords='offset points')
    ax.get_yaxis().set_ticks([])
    plt.xlabel('')

    fig.add_subplot(122)
    plt.axis('off')
    p = gr.loc[:,'{} Ratio'.format(col)].plot(kind= 'pie',
                                     autopct='%1.1f%%',shadow=False,
                                     title='{} Ratio'.format(title), legend=False, labels=None);

    sns.despine(top=True, right=True, left=True, bottom=False);