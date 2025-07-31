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
    field: 'pay_company',
    label: '代付公司',
    colProps: {
      span: 23
    },
    component: 'Input'
  },
  {
    field: 'name',
    label: '公司名称',
	component: 'Input',
    colProps: {
      span: 23
    }
    
  },
  {
    field: 'channel_name',
    label: '通道名称',
    colProps: {
      span: 23
    },
    component: 'Input'
  },
  // {
  //   field: 'channel_account',
  //   label: '通道账号',
  //   colProps: {
  //     span: 23
  //   },
  //   component: 'Input'
  // },
  // {
  //   field: 'channel_pwd',
  //   label: '通道密码',
  //   colProps: {
  //     span: 23
  //   },
  //   component: 'Input'
  // },
  {
    field: 'channel_code',
    label: '通道code',
    colProps: {
      span: 23
    },
    component: 'Input'
  },
  {
    field: 'channel_type',
    label: '通道类型',
    colProps: {
      span: 23
    },
    component: 'Select',
	componentProps: {
	  options: [
	    {
	      label: '代收通道',
	      value: 1
	    },
	    {
	      label: '代付通道',
	      value: 2
	    }
	  ]
	}
  },
  // {
  //   field: 'amount_type',
  //   label: '金额类型',
  //   colProps: {
  //     span: 23
  //   },
  //   component: 'Select',
  // 	componentProps: {
  // 	  options: [
  // 	    {
  // 	      label: '大金额',
  // 	      value: 1
  // 	    },
  // 	    {
  // 	      label: '小金额',
  // 	      value: 2
  // 	    }
  // 	  ]
  // 	}
  // },
  {
    field: 'channel_status',
    label: '通道状态',
    colProps: {
      span: 23
    },
    component: 'Select',
	componentProps: {
	  options: [
	    {
	      label: '正常',
	      value: 1
	    },
	    {
	      label: '异常',
	      value: 2
	    }
	  ]
	}
  },
  // {
  //   field: 'upi_business_code',
  //   label: 'upi业务编码',
  //   colProps: {
  //     span: 23
  //   },
  //   component: 'Input'
  // },
  {
    field: 'pay_gw_addr',
    label: '代付网关地址',
    colProps: {
      span: 23
    },
    component: 'Input'
  },


  {
    field: 'pay_gw_check_status_addr',
    label: '代付网关状态检查地址',
    colProps: {
      span: 23
    },
    component: 'Input'
  },
  {
    field: 'pay_gw_merchant_id',
    label: '代付网关商户名称(ID)',
    colProps: {
      span: 23
    },
    component: 'Input'
  },
  {
    field: 'pay_gw_id',
    label: '代付网关ID(key)',
    colProps: {
      span: 23
    },
    component: 'Input'
  },
  
  {
    field: 'pay_gw_token',
    label: '代付网关TOKEN(secret)',
    colProps: {
      span: 23
    },
    component: 'Input'
  },
  
  {
    field: 'pay_gw_callback_id',
    label: '代付网关回调地址ID',
    colProps: {
      span: 23
    },
    component: 'Input'
  },
  {
    field: 'pay_gw_spare',
    label: '支付网关备用字段',
    colProps: {
      span: 23
    },
    component: 'Input'
  },

  
  // {
  //   field: 'disabled',
  //   label: '是否禁用',
  //   colProps: {
  //     span: 12
  //   },
  //   component: 'RadioGroup',
  //   componentProps: {
  //     style: {
  //       width: '100%'
  //     },
  //     options: [
  //       {
  //         label: '正常',
  //         value: true
  //       },
  //       {
  //         label: '禁用',
  //         value: false
  //       }
  //     ]
  //   },
  //   value: true
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
  pay_company: [required()],
  channel_name: [required()],
  channel_code: [required()],
  channel_type: [required()],
  channel_status: [required()],
  // amount_type: [required()]
  
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
