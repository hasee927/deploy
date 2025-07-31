<script setup lang="tsx">
import { Form, FormSchema } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { PropType, reactive, watch } from 'vue'
import { useValidator } from '@/hooks/web/useValidator'


const { required } = useValidator()

const props = defineProps({
  currentRow: {
    type: Object as PropType<any>,
    default: () => null
  }
})



const formSchema = reactive<FormSchema[]>([
  {
    field: 'name',
    label: '银行名称',
    colProps: {
      span: 23
    },
    component: 'Input'
  },
  {
    field: 'desc',
    label: '描述',
	component: 'Input',
    colProps: {
      span: 23
    }
  },
  {
    field: 'image',
    label: '图标URL',
  	component: 'Input',
    colProps: {
      span: 23
    }
  },
  
  
])

const rules = reactive({
  name: [required()],
  desc: [required()],
  
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
  },
  {
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
