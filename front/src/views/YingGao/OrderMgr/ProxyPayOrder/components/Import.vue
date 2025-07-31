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





const formSchema = reactive<FormSchema[]>([

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
		  // action: "https://api.magicpay.click/yg/pporder/uploadpayout",
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

const rules = reactive({
  bank_name: [required()],  
})

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
