<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import { ElSwitch } from 'element-plus'
import { Search } from '@/components/Search'
import { FormSchema } from '@/components/Form'
import { ContentWrap } from '@/components/ContentWrap'
import Write from './components/Write.vue'
import { Dialog } from '@/components/Dialog'
import { BaseButton } from '@/components/Button'

import { getFinanceApi, getFinanceByIdApi, editFinanceApi } from '@/api/yinggao/finance/finance'

const auth = JSON.parse(localStorage.getItem("auth"))
const showOpertionMenu = ref(true)

const width = 120;

const { t } = useI18n()

const channelList = ref()

const changeShowMenu = async () => {
	if(auth.user.nickname == 'merchant'){
		showOpertionMenu.value = false
	}
}

changeShowMenu()

const { tableRegister, tableState, tableMethods } = useTable({
  // 获取商户列表
  fetchDataApi: async () => {
	const { pageSize, currentPage } = tableState
	const jsonData = {
      page: unref(currentPage),
      limit: unref(pageSize),
      ...unref(searchParams)
    }

	if(auth.user.nickname == 'merchant'){
		jsonData['merchant_id'] = auth.user.name
	}
	
    const res = await getFinanceApi(jsonData)
    return {
      list: res.data || [],
      total: res.count || 0
    }
  },

  

})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList, delList } = tableMethods



const tableColumns = reactive<TableColumn[]>([
  {
    field: 'merchant_id',
    label: '商户ID',
    show: true,
  },

  {
    field: 'total_amount',
    label: '总金额',
    show: true,
  },

 {
   field: 'change_fund',
   label: '可转换资金',
   show: true,
 },
 
 {
   field: 'pay_amount',
   label: '可用代付金额',
   show: true,
 },
 
 {
   field: 'pending_amount',
   label: '在途金额(pending)',
   show: true,
 },
 
 {
   field: 'remark',
   label: '备注',
   show: true,
 },
 
 {
   field: 'action',
   width: '160px',
   label: '操作',
   show: showOpertionMenu,
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
             调账
           </BaseButton>
         </>
       )
     }
   }
 }

])

const searchSchema = reactive<FormSchema[]>([

  {
    field: 'merchant_id',
    label: '商户ID',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  }
  

])

const searchParams = ref({})
const setSearchParams = (data: any) => {
  var dates = data["dates"]

  currentPage.value = 1
  searchParams.value = data
  getList()
}




const dialogVisible = ref(false)
const dialogTitle = ref('')

const currentRow = ref()
const actionType = ref('')

const writeRef = ref<ComponentRef<typeof Write>>()

const saveLoading = ref(false)

const editAction = async (row: any) => {
  
  const res = await getFinanceByIdApi(row.id)
  if (res) {
	const data  = res.data
	data['change_type'] = undefined
	data['change_amount'] = undefined
    dialogTitle.value = '调账'
    actionType.value = 'edit'
    currentRow.value = data
    dialogVisible.value = true
  }
}


const save = async () => {
  const write = unref(writeRef)
  var formData = await write?.submit()
  if (formData) {
    saveLoading.value = true
    try {
      const res = ref({})
      if (actionType.value === 'edit') {
        res.value = await editFinanceApi(formData)
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
