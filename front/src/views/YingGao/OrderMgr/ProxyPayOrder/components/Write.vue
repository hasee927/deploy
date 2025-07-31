<script setup lang="tsx">
import { Form, FormSchema } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { PropType, reactive, ref, watch } from 'vue'
import { useValidator } from '@/hooks/web/useValidator'

import { forEach } from 'lodash'


const {required} = useValidator()

const props = defineProps({
	currentRow: {
		type: Object as PropType < any > ,
		default: () => null
	}
})



const formSchema = reactive < FormSchema[] > ([

	  {
		field: 'bank_name',
		label: '选择银行',
		colProps: {
		  span: 23
		},
		component: 'Select',
		componentProps: {
		  options: [
			{
			  label: 'IOB',
			  value: 'IOB'
			},
			{
			  label: 'IDFC',
			  value: 'IDFC'
			},
		  ]
		}
	  },


])



const rules = reactive({
  bank_name: [required()],  
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