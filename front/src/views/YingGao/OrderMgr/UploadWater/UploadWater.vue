<script setup lang="tsx">
import { ContentWrap } from '@/components/ContentWrap'
import { useI18n } from '@/hooks/web/useI18n'
import { Table } from '@/components/Table'
import Write from './components/Write.vue'
import Create from './components/CreateEdit.vue'
// import { ElSwitch, ElMessage  ,ElOption,
//   ElOptionGroup,
//   ElRadio,
//   ElRadioButton,
//   ElCheckbox,
//   ElCheckboxButton,
//   ElInput,
//   ElMessageBox,
//   ElIcon} from 'element-plus'
import { imPortCsvDataApi, getBtnListApi, getBtnByIdApi, addBtnApi, editBtnApi, delBtnApi } from '@/api/yinggao/orderMgr/banklist'
// import { getCardTableListApi } from '@/api/table'
import { ref, unref } from 'vue'
import { ElLink, ElDivider, ElMessageBox, ElMessage } from 'element-plus'
import { Dialog } from '@/components/Dialog'
import { Search } from '@/components/Search'

interface Params {
  pageIndex?: number
  pageSize?: number
}

const { t } = useI18n()

// const loading = ref(true)

const tableDataList = ref<any[]>([])

// tableDataList.value = [{"name": "PIOB", "desc": "点击，上传IOB银行流水，格式csv"}, {"name": "PBOM", "desc": "点击，上传BOM银行流水，格式xls"}]


const getTableList = async () => {
  const res = await getBtnListApi()

  if (res) {
    tableDataList.value = res.data
  }
}
getTableList()


const writeRef = ref<ComponentRef<typeof Write>>()
const createRef = ref<ComponentRef<typeof Create>>()

const saveLoading = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const currentRow = ref()
const actionType = ref('')
const bank_name = ref()

const actionClick = (row?: any) => {
  bank_name.value = row
  dialogTitle.value = '上传'+row
  actionType.value = 'upload'
  currentRow.value = undefined
  dialogVisible.value = true
}

const save = async () => {
  const write = unref(writeRef)
  const formData = await write?.submit()
  // console.log("formData------------->", formData)

  if (formData) {
	const jsonData = {
	  	"bank_name": bank_name.value,
	  	"bank_account": formData.bank_account,
	  	"channel_code": formData.channel_code,
	  	"file_name": formData.upload_file[0].name
	}
    saveLoading.value = true
    try {
      const res = ref({})
      if (actionType.value === 'upload') {
        res.value = await imPortCsvDataApi(jsonData)
        if (res.value) {
          dialogVisible.value = false
		  ElMessage({
		  	type: 'success',
		  	message: '上传成功',
		  })
        }else{
			dialogVisible.value = false
			ElMessage({
				type: 'error',
				message: '上传失败',
			})
		}
      }
    } finally {
      saveLoading.value = false
    }
  }
}


const editdialogVisible = ref(false)
const editdialogTitle = ref('')
const editactionType = ref('')
const editcurrentRow = ref()


const addAction = () => {
  editdialogTitle.value = '新增'
  editactionType.value = 'add'
  editcurrentRow.value = undefined
  editdialogVisible.value = true
}

const editAction = async (row: any) => {
  const res = await getBtnByIdApi(row.id)
  if (res) {
	  editdialogTitle.value = '编辑'
	  editactionType.value = 'edit'
	  editcurrentRow.value = row
	  editdialogVisible.value = true
  }

}


const submit = async () => {
  const write = unref(createRef)
  const formData = await write?.submit()

  if (formData) {
    saveLoading.value = true
    try {
      const res = ref({})
      if (editactionType.value === 'add') {
        res.value = await addBtnApi(formData)
        if (res.value) {
          editdialogVisible.value = false
		  getTableList()
        }
      } else if (editactionType.value === 'edit') {
        res.value = await editBtnApi(formData)
        if (res.value) {
          editdialogVisible.value = false
          getTableList()
        }
      }
    } finally {
      saveLoading.value = false
    }
  }
}


const delLoading = ref(false)
const delData = async (row: any) => {

	ElMessageBox.confirm(
		'确定删除该数据！',
		'系统提示',
		{  
			confirmButtonText: '确定',
			cancelButtonText: '取消',
			type: 'warning',
		}).then(async () => {
			delLoading.value = true
			const res = await delBtnApi([row.id])
			if (res) {
				ElMessage({
					type: 'success',
					message: '删除成功',
				})
				getTableList()
				delLoading.value = false
			}else{
				ElMessage({
					type: 'error',
					message: '删除失败',
				})
				delLoading.value = false
			}
			
		}).catch(() => {
			ElMessage({
				type: 'info',
				message: '取消删除',
			})
			delLoading.value = false
		})

}


</script>

<template>
  <ContentWrap :title="t('上传银行流水')">

	<div style="margin-bottom: 20px;">
		<BaseButton type="primary" @click="addAction">新增</BaseButton>
	</div>


    <Table
      :columns="[]"
      :data="tableDataList"

      custom-content
      :card-wrap-style="{
        width: '200px',
        marginBottom: '20px',
        marginRight: '20px'
      }"
    >
	
	
    <template #content="row">
        <div class="flex cursor-pointer" @click="actionClick(row.name)">
          <div class="pr-16px" style="margin-top: 20px;">
			  <span v-if="row.image">
				  <img  :src="row.image" class="w-48px h-48px rounded-[50%]" alt="" />
			  </span>
			  <span v-else>
				  <img  src="/public/logo.jpg" class="w-48px h-48px rounded-[50%]" alt="" />
			  </span>
          </div>
          <div>
			  <!-- 409eff -->
            <div class="mb-12px font-700 font-size-16px color-[#5e5e5e]">{{ row.name }}</div>
            <div class="line-clamp-3 font-size-12px" style="display: flex; flex-direction: column;">
				<el-button size="small" type="primary">点击上传</el-button>
				<span style="margin-top: 10px; font-weight: bold; color: #999;">{{ row.desc }}</span>
			</div>
          </div>
        </div>
    </template>
	<template #content-footer="item">
        <div class="flex justify-center items-center">
          <div class="flex-1 text-center" @click="() => editAction(item)">
			<el-button size="small" type="success">编辑</el-button>
          </div>
          <ElDivider direction="vertical" />
          <div class="flex-1 text-center" @click="() => delData(item)">
			<el-button size="small" type="danger" :loading="delLoading">删除</el-button>			
          </div>
        </div>
      </template>
    </Table>
  </ContentWrap>
  
  <Dialog v-model="dialogVisible" :title="dialogTitle" :height="300">
     <Write ref="writeRef" :current-row="currentRow" />
  
     <template #footer>
       <BaseButton type="primary" :loading="saveLoading" @click="save">
         {{ t('exampleDemo.save') }}
       </BaseButton>
       <BaseButton @click="dialogVisible = false">{{ t('dialogDemo.close') }}</BaseButton>
     </template>
   </Dialog>
  
  <!-- 添加编辑 -->
  <Dialog v-model="editdialogVisible" :title="editdialogTitle" :height="300">
     <Create ref="createRef" :current-row="editcurrentRow" />
  
     <template #footer>
       <BaseButton type="primary" :loading="saveLoading" @click="submit">
         {{ t('exampleDemo.save') }}
       </BaseButton>
       <BaseButton @click="editdialogVisible = false">{{ t('dialogDemo.close') }}</BaseButton>
     </template>
   </Dialog>
  
  
</template>
