<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import { getOrderstatApi } from '@/api/yinggao/orderMgr/orderstat'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import { ElSwitch, ElMessage } from 'element-plus'
import { Search } from '@/components/Search'
import { FormSchema } from '@/components/Form'
import { ContentWrap } from '@/components/ContentWrap'
import { Dialog } from '@/components/Dialog'
import { BaseButton } from '@/components/Button'

const { t } = useI18n()


const { tableRegister, tableState, tableMethods } = useTable({
  // 获取成功订单列表
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getOrderstatApi({
      page: unref(currentPage),
      limit: unref(pageSize),
      ...unref(searchParams)
    })
    return {
      list: res.data || [],
      total: res.count || 0
    }
  },

})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList, delList } = tableMethods

// 定时刷新成功率
const queryInterval = setInterval(() => {
		getList();
}, 600000);

const searchSchema = reactive<FormSchema[]>([
  {
    field: 'bank_name',
    label: '银行名称',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'channel_code',
    label: '通道名称',
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
  currentPage.value = 1
  searchParams.value = data
  getList()
}

const tableColumns = reactive<TableColumn[]>([
  {
    field: 'bank_name',
    label: '银行名称',
    show: true,
  },
  {
    field: 'channel_code',
    label: '通道名称',
    show: true,
  },
  {
    field: 'success_order',
    label: '成功订单数',
    show: true,
	width: '200px'
  },
  {
    field: 'fail_order',
    label: '失败订单数',
    show: true,
  },
  {
    field: 'total_order',
    label: '总订单数',
    show: true,
  },
  {
    field: 'success_rate',
    label: '成功率',
    show: true,
  },
  {
    field: 'success_amount',
    label: '成功金额',
    show: true,
  },
  {
    field: 'total_amount',
    label: '订单总金额',
    show: true,
  },
  {
    field: 'create_datetime',
    label: '创建时间',
    show: true,
  }
   
   
 
])





const dialogVisible = ref(false)
const dialogTitle = ref('')

const currentRow = ref()
const actionType = ref('')


const saveLoading = ref(false)



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

</template>
