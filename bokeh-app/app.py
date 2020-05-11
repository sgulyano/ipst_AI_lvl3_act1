import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, RadioButtonGroup, Div, Paragraph
from bokeh.plotting import figure
from bokeh.transform import factor_cmap, factor_mark

from sklearn.datasets import load_breast_cancer

np.random.seed(42)

##
data = load_breast_cancer()
X = data['data'][:, :2]
y = data['target']


x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1

idx = np.random.choice(np.where(y == 0)[0], size=int(
    np.sum(y == 1)*0.1), replace=False)

noise = np.random.normal(0, 0.1, (idx.size*10, 2))
noise[:idx.size, :] = 0

x_train = np.concatenate((X[y == 1], X[idx]))
y_train = np.concatenate((y[y == 1], y[idx]))

y_map_value = {k:v for k, v in enumerate(data.target_names)}
y_set = data.target_names
y_train_name = [y_map_value[y] for y in y_train]

# Set up data
source = ColumnDataSource(data=dict(x=x_train[:,0], y=x_train[:,1], c=y_train_name))


# Set up plot
plot = figure(plot_height=400, plot_width=600,
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[x_min, x_max], y_range=[y_min, y_max])

plot.scatter('x', 'y', source=source, legend_field="c", fill_alpha=0.4, size=12, 
             marker=factor_mark('c', ['hex', 'triangle'], y_set),
             color=factor_cmap('c', 'Category10_3', y_set))


title = Div(text="""<H1>จำนวนข้อมูลที่ไม่สมดุลกัน (Imbalanced Data)</H1>""")
desc = Paragraph(text="""ในแบบฝึกหัดนี้ ให้นักเรียนลองใช้เทคนิค 1) การสุ่มข้อมูลจากกลุ่มหลักให้มีน้อยลง (Under-Sampling) และ 2) 
การสร้างข้อมูลของกลุ่มย่อยให้มีมากขึ้น (Over-Sampling) แล้วลองสังเกต Decision Tree ผลลัพธ์ ที่ได้""")
header = column(title, desc, sizing_mode="scale_both")




# Set up widgets
text = Div(text="<H3>ตัวแปร</H3>")
underspl = Slider(title="Under-Sampling", value=100, start=10, end=100, step=10)
overspl = Slider(title="Over-Sampling", value=100, start=100, end=1000, step=100)


def set_source_value(x_new, y_new):
    y_train_name = [y_map_value[y] for y in y_new]
    source.data = dict(x=x_new[:,0], y=x_new[:,1], c=y_train_name)

def under_sampling(attrname, old, new):
    ratio = underspl.value
    num = int(np.sum(y_train == 1)*ratio/100.0)
    idx = np.where(y_train == 1)[0][:num]

    x_new = np.concatenate((x_train[y_train == 0], x_train[idx]))
    y_new = np.concatenate((y_train[y_train == 0], y_train[idx]))

    set_source_value(x_new, y_new)

underspl.on_change('value', under_sampling)




decbound_text = Paragraph(text="ขอบเขตการจำแนก")
decbound = RadioButtonGroup(labels=["ซ่อน", "แสดง"], active=0)

# Set up layouts and add to document
inputs = column(text, underspl, overspl, decbound_text, decbound)
body = row(inputs, plot, width=800)

curdoc().add_root(column(header, body))
curdoc().title = "จำนวนข้อมูลที่ไม่สมดุลกัน"