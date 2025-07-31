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


// 获取所有节点的key
const getTreeNodeKeys = (nodes: Recordable[]): number[] => {
  let keys = [] as number[]
  for (let i = 0; i < nodes.length; i++) {
    keys.push(nodes[i].value)
    if (nodes[i].children && nodes[i].children.length > 0) {
      keys = keys.concat(getTreeNodeKeys(nodes[i].children))
    }
  }
  return keys
}



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
    field: 'token',
    label: '机器人TOKEN',
	component: 'Input',
    colProps: {
      span: 23
    }
    
  },
  {
    field: 'user_to',
    label: '用途',
    colProps: {
      span: 23
    },
    component: 'Input'
  },
  {
    field: 'command',
    label: '机器人命令',
    colProps: {
      span: 23
    },
    component: 'Input'
  },
  {
    field: 'bot_sign',
    label: '机器人标识',
    colProps: {
      span: 23
    },
    component: 'Input'
  },
  {
    field: 'sign',
    label: '接口签名',
    colProps: {
      span: 23
    },
    component: 'Input'
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
  pay_company: [required()],
  channel_name: [required()],
  channel_code: [required()],
  channel_type: [required()],
  channel_status: [required()],
  disabled: [required()]
  
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
