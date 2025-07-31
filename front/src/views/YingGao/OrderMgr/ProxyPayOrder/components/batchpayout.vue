<script setup lang="tsx">
import { Form, FormSchema } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { PropType, reactive, ref, watch } from 'vue'
import { useValidator } from '@/hooks/web/useValidator'
import { forEach } from 'lodash'
import { getBigPayChannelOptionsApi } from '@/api/yinggao/merchantMgr/channel'


const {required} = useValidator()

const props = defineProps({
	currentRow: {
		type: Object as PropType < any > ,
		default: () => null
	}
})




const formSchema = reactive < FormSchema[] > ([


  {
    field: 'total_amount',
    label: '出款总金额',
    colProps: {
      span: 23
    },
    component: 'Input',
	value: '#',
	componentProps: {
	  disabled: true
	}
  },
  
  {
    field: 'failNum',
    label: '出款失败停止数量',
    colProps: {
      span: 23
    },
    component: 'Input',
  },
  

	 {
		field: 'pay_channel_code',
		label: '代付通道组',
		colProps: {
		  span: 23
		},
		component: 'Select',
		componentProps: {
		  style: {
			width: '100%'
		  },
		  multiple: false
		},
		optionApi: async () => {
		  // 获取通道列表
		  const res = await getBigPayChannelOptionsApi()
		  res.data.forEach(item => {
		    item['value'] = item['label']
		  });
		  
		  return res.data
		},
		value: [],

	  },

])



const rules = reactive({

})


const { formRegister, formMethods } = useForm()
const { setValues, getFormData, getElFormExpose } = formMethods

const submit = async () => {
	const elForm = await getElFormExpose()
	const valid = await elForm?.validate()
	if (valid) {
		const formData = await getFormData()
		return formData
	}
}

watch(
	() => props.currentRow,
	(currentRow) => {
		if (!currentRow) return
		setValues(currentRow)
	}, {
		deep: true,
		immediate: true
	}
)



defineExpose({
	submit
})
</script>

<template>
	<Form :rules="rules" @register="formRegister" :schema="formSchema" />
</template>