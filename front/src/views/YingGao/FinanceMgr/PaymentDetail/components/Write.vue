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
    field: 'channel_code',
    label: '打款通道',
    colProps: {
      span: 23
    },
    component: 'Input'
  },
  {
    field: 'payment_code',
    label: '收款通道',
	component: 'Input',
    colProps: {
      span: 23
    }
    
  },
  {
    field: 'amount',
    label: '打款金额',
    colProps: {
      span: 23
    },
    component: 'Input'
  },
  
  // {
  //   field: 'return_u',
  //   label: '回U',
  //   colProps: {
  //     span: 23
  //   },
  //   component: 'Input'
  // },
  
  {
    field: 'remark',
    label: '备注',
    colProps: {
      span: 23
    },
    component: 'Input',
    componentProps: {
      rows: 1,
      type: 'textarea',
      style: {
        width: '600px'
      }
    }
  }
  
])

const rules = reactive({
  channel_code: [required()],
  payment_code: [required()],
  amount: [required()]
  
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
