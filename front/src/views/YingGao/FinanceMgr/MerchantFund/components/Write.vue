<script setup lang="tsx">
import { Form, FormSchema } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { PropType, reactive, ref, watch } from 'vue'
import { useValidator } from '@/hooks/web/useValidator'



var { required } = useValidator()

const props = defineProps({
  currentRow: {
    type: Object as PropType<any>,
    default: () => null
  }
})


// 获取所有节点的key
// const getTreeNodeKeys = (nodes: Recordable[]): number[] => {
//   let keys = [] as number[]
//   for (let i = 0; i < nodes.length; i++) {
//     keys.push(nodes[i].value)
//     if (nodes[i].children && nodes[i].children.length > 0) {
//       keys = keys.concat(getTreeNodeKeys(nodes[i].children))
//     }
//   }
//   return keys
// }



const formSchema = reactive<FormSchema[]>([
  {
    field: 'total_amount',
    label: '总金额',
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
    field: 'pending_amount',
    label: '在途金额',
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
    field: 'pay_amount',
    label: '代付金额',
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
    field: 'change_fund',
    label: '可转换资金',
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
    field: 'change_type',
    label: '调整类型',
    colProps: {
      span: 23
    },
    component: 'Select',
    componentProps: {
      options: [
        {
          label: '划扣',
          value: 0
        },
        {
          label: '上分',
          value: 1
        },
		{
		  label: '可用转代付',
		  value: 2
		},
		{
		  label: '代付转可用',
		  value: 3
		}
      ]
    }
  },
  {
    field: 'change_amount',
    label: '变动金额',
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
	total_amount: [required()],
	pending_amount: [required()],
	pay_amount: [required()],
	change_fund: [required()],
	change_type: [required()],
	change_amount: [required()],

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
   <!-- <Form @register="formRegister" :schema="formSchema" /> -->
</template>
