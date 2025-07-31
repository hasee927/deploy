<script setup lang="tsx">
import { Form, FormSchema } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { PropType, reactive, watch } from 'vue'
import { useValidator } from '@/hooks/web/useValidator'
import { BaseButton } from '@/components/Button'
import { ElMessage, ElMessageBox } from 'element-plus'
import { upLoadFileApi } from '@/api/yinggao/orderMgr/banklist'




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
    field: 'bank_account',
    label: '银行账号',
	component: 'Input',
    colProps: {
      span: 23
    }
    
  },
  {
    field: 'channel_code',
    label: '通道code',
  	component: 'Input',
    colProps: {
      span: 23
    }
  },
  {
	field: 'upload_file',
    label: '上传文件',
  	component: 'Upload',
    colProps: {
      span: 23
    },	
	componentProps: {
	      limit: 1,
	      // action: upLoadFileApi,
		  action: import.meta.env.VITE_UPLOAD_BANK_DATA,
	      // fileList: ,
	      multiple: false,
	      onPreview: (uploadFile) => {
	        console.log(uploadFile)
	      },
	      onRemove: (file) => {
	        console.log(file)
	      },
	      beforeRemove: (uploadFile) => {
	        return ElMessageBox.confirm(`Cancel the transfer of ${uploadFile.name} ?`).then(
	          () => true,
	          () => false
	        )
	      },
	      onExceed: (files, uploadFiles) => {
	        ElMessage.warning(
	          // `The limit is 1, you selected ${files.length} files this time, add up to ${
	          //   files.length + uploadFiles.length
	          // } totally`
			  `只能上传一个文件！`
	        )
	      },
	      slots: {
	        default: () => <BaseButton type="primary">Click to upload</BaseButton>,
	        // tip: () => <div class="el-upload__tip">jpg/png files with a size less than 500KB.</div>
	      }
	    }
  },

  
])


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
  <!-- <Form :rules="rules" @register="formRegister" :schema="formSchema" /> -->
  <Form @register="formRegister" :schema="formSchema" />
  
</template>
