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
    field: 'chat_id',
    label: '群聊ID',
    colProps: {
      span: 23
    },
    component: 'Input'
  },
  {
    field: 'name',
    label: '群名称',
    colProps: {
      span: 23
    },
    component: 'Input'
  },

  {
    field: 'type',
    label: '群类型',
    colProps: {
      span: 23
    },
    component: 'Select',
	componentProps: {
	  options: [
	    {
	      label: '商户',
	      value: 1
	    },
	    {
	      label: '渠道',
	      value: 2
	    }
	  ]
	}
  },
  {
    field: 'disabled',
    label: '是否禁用',
    colProps: {
      span: 12
    },
    component: 'RadioGroup',
    componentProps: {
      style: {
        width: '100%'
      },
      options: [
        {
          label: '启用',
          value: true
        },
        {
          label: '禁用',
          value: false
        }
      ]
    },
    value: true
  },
 
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
