<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import {
  getPayDetailListApi,
  getPayDetailByIdApi,
  addPayDetailApi,
  editPayDetailApi,
  delPayDetailApi,
  exportDatalApi
} from '@/api/yinggao/finance/paymentdetail'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import { ElSwitch, ElMessage } from 'element-plus'
import { Search } from '@/components/Search'
import { FormSchema } from '@/components/Form'
import { ContentWrap } from '@/components/ContentWrap'
import Write from './components/Write.vue'
import { Dialog } from '@/components/Dialog'
import { BaseButton } from '@/components/Button'



const { t } = useI18n()

const { tableRegister, tableState, tableMethods } = useTable({
  // 获取打款明细列表
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getPayDetailListApi({
      page: unref(currentPage),
      limit: unref(pageSize),
      ...unref(searchParams)
    })
    return {
      list: res.data || [],
      total: res.count || 0
    }
  },
  
  // 删除通道
  fetchDelApi: async (value) => {
    const res = await delPayDetailApi(value)
    return res.code === 200
  },
  
})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList, delList } = tableMethods



const tableColumns = reactive<TableColumn[]>([
  {
    field: 'channel_code',
    label: '打款通道',
    show: true,
  },
  {
    field: 'payment_code',
    label: '收款通道',
    show: true,
  },
  {
    field: 'amount',
    label: '打款金额',
    show: true,
  },

  // {
  //   field: 'return_u',
  //   label: '回U',
  //   show: true,
  // },

  {
    field: 'create_datetime',
    label: '创建时间',
    show: true
  },
  {
    field: 'remark',
    label: '备注',
    show: true,
  
  },
  {
    field: 'action',
    width: '170px',
    label: '操作',
    show: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <BaseButton
              type="primary"
              link
              size="small"
              onClick={() => editAction(row)}
            >
              编辑
            </BaseButton>
            <BaseButton
              type="danger"
              loading={delLoading.value}
              link
              size="small"
              onClick={() => delData(row)}
            >
              删除
            </BaseButton>
          </>
        )
      }
    }
  }
])

const searchSchema = reactive<FormSchema[]>([
  {
    field: 'channel_code',
    label: '打款通道',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'payment_code',
    label: '收款通道',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'from_date',
    component: 'DatePicker',
  	label: "选择时间",
	componentProps: {
		  type: 'datetimerange',
		}
    },

])



const formatDate = (date: any) => {
    let year = date.getFullYear();
    let month = String(date.getMonth() + 1).padStart(2, '0'); // 月份是从0开始的
    let day = String(date.getDate()).padStart(2, '0');
    let hours = String(date.getHours()).padStart(2, '0');
    let minutes = String(date.getMinutes()).padStart(2, '0');
    let seconds = String(date.getSeconds()).padStart(2, '0');
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

const searchParams = ref({})
const setSearchParams = (data: any) => {
	if(Object.keys(data).length != 0) {
		if(data['from_date']) {
			const tempList = []
			data['from_date'].forEach((item) =>{
				const date = new Date(item)
				const row = formatDate(date)
				tempList.push(row)
			})
			
			data['from_date'] = tempList[0]
			data['to_date'] = tempList[1]
		}

	}

	currentPage.value = 1
	searchParams.value = data
	getList()
}

const delLoading = ref(false)

const delData = async (row: any) => {
  delLoading.value = true
  await delList(true, [row.id]).finally(() => {
    delLoading.value = false
  })
}



const dialogVisible = ref(false)
const dialogTitle = ref('')

const currentRow = ref()
const actionType = ref('')

const writeRef = ref<ComponentRef<typeof Write>>()

const saveLoading = ref(false)

const editAction = async (row: any) => {
  const res = await getPayDetailByIdApi(row.id)
  if (res) {
    dialogTitle.value = '编辑'
    actionType.value = 'edit'
    currentRow.value = res.data
    dialogVisible.value = true
  }
}

const addAction = () => {
  dialogTitle.value = '新增'
  actionType.value = 'add'
  currentRow.value = undefined
  dialogVisible.value = true
}

const save = async () => {
  const write = unref(writeRef)
  const formData = await write?.submit()
  if (formData) {
    saveLoading.value = true
    try {
      const res = ref({})
      if (actionType.value === 'add') {
        res.value = await addPayDetailApi(formData)
        if (res.value) {
          dialogVisible.value = false
          getList()
        }
      } else if (actionType.value === 'edit') {
        res.value = await editPayDetailApi(formData)
        if (res.value) {
          dialogVisible.value = false
          getList()
        }
      }
    } finally {
      saveLoading.value = false
    }
  }
}


const exportQueryList = async (data) => {
	console.log("searchParams----->>", searchParams.value)
	const formData = searchParams.value

	try {
	  loading.value = true
	  const res = await exportDatalApi(formData)
	  if (res) {
		const a = document.createElement('a')
		a.style.display = 'none'
		a.href = res.data.url
		a.target = '_blank'
		a.download = res.data.filename
		const event = new MouseEvent('click')
		a.dispatchEvent(event)
		
		ElMessage({
			type: 'success',
			message: '导出成功',
		})
		dialogVisible.value = false
		// getList()
	  }
	} catch (err) {
	  console.log('bankExportApi error')
	} finally {
	  loading.value = false
	}

}


</script>

<template>
  <ContentWrap>
    <Search :schema="searchSchema" @reset="setSearchParams" @search="setSearchParams" />
    <Table
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      showAction
      :columns="tableColumns"
      default-expand-all
      node-key="id"
      :data="dataList"
      :loading="loading"
      :pagination="{
        total
      }"
      @register="tableRegister"
      @refresh="getList"
    >
      <template #toolbar>
        <ElRow :gutter="10">
          <ElCol :span="1.5">
            <BaseButton type="primary" v-hasPermi="['merchant.channel.create']" @click="addAction">新增</BaseButton>
          </ElCol>
		  <ElCol :span="1.5">
		    <BaseButton type="success" @click="exportQueryList">导出</BaseButton>
		  </ElCol>
        </ElRow>
      </template>
    </Table>
  </ContentWrap>

  <Dialog v-model="dialogVisible" :title="dialogTitle" :height="500">
    <Write ref="writeRef" :current-row="currentRow" />

    <template #footer>
      <BaseButton type="primary" :loading="saveLoading" @click="save">
        {{ t('exampleDemo.save') }}
      </BaseButton>
      <BaseButton @click="dialogVisible = false">{{ t('dialogDemo.close') }}</BaseButton>
    </template>
  </Dialog>

  <!-- <AuthManage ref="authManageRef" :current-row="currentRow" @get-list="getList" /> -->
</template>
