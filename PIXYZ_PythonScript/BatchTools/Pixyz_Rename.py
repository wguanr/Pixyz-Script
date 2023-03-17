import pixyz
from pixyz.utils import get_dict_values

# 定义模型输入
model_input = pixyz.input_spec(shape=(None, 3))

# 定义模型
model = pixyz.Model(
    get_dict_values(model_input),
    name='rename_materials'
)

# 定义模型流程
def rename_materials(x):
    materials = x['materials']
    new_names = x['new_names']
    for i in range(materials.shape[0]):
        materials[i].name = new_names[i]
    return {'renamed_materials': materials}

model.rename_materials = rename_materials

# 使用模型进行重命名
input_data = {'materials': ['mat_1', 'mat_2', 'mat_3'], 'new_names': ['red', 'green', 'blue']}
output_data = model.sample(input_data)
renamed_materials = output_data['renamed_materials']

# 打印重命名后的材质名称
print(renamed_materials)
