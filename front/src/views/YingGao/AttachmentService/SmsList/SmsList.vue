<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import { getSmsListApi } from '@/api/yinggao/AttachmentService/smslist'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import { ElSwitch } from 'element-plus'
import { Search } from '@/components/Search'
import { FormSchema } from '@/components/Form'
import { ContentWrap } from '@/components/ContentWrap'
import { BaseButton } from '@/components/Button'



const { t } = useI18n()

const { tableRegister, tableState, tableMethods } = useTable({
  // 获取通道列表
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getSmsListApi({
      page: unref(currentPage),
      limit: unref(pageSize),
      ...unref(searchParams)
    })
    return {
      list: res.data || [],
      total: res.count || 0
    }
  }
})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList } = tableMethods



const tableColumns = reactive<TableColumn[]>([
	{
		field: 'channel_code',
		label: '通道CODE',
		width: '160px',
		show: true,
	},
	{
		field: 'sms_time',
		label: '短信时间',
		width: '200px',
		show: true
	},

	{
		field: 'sender_addr',
		label: '发送人',
		width: '180px',
		show: true,
	},
	{
		field: 'sms_type',
		label: '短信类型',
		width: '170px',
		show: true,
		slots: {
		  default: (data: any) => {
		    const row = data.row
			if(row.sms_type == 1) {
				return (<><span><el-button type="default" size="small" plain>其他短信</el-button></span></>)
			}else{
				return (<><span><el-button type="success" size="small" plain>OTP短信</el-button></span></>)
			}
		  }
		}
	},
	{
		field: 'code',
		label: 'OTP验证码',
		width: '160px',
		show: true,
	},


	{
		field: 'context',
		label: '短信内容',
		width: '800px',
		show: true,
	},

])

const searchSchema = reactive<FormSchema[]>([
  {
    field: 'channel_code',
    label: '通道code',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'sms_type',
    label: '短信类型',
    component: 'Select',
    componentProps: {
      style: {
        width: '214px'
      },
      options: [
        {
          label: '其他短信',
          value: 1
        },
        {
          label: 'otp短信',
          value: 2
        }
      ]
    }
  },
  {
    field: 'context',
    label: '短信内容',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },
])

const searchParams = ref({})
const setSearchParams = (data: any) => {
  currentPage.value = 1
  searchParams.value = data
  getList()
}

const delLoading = ref(false)




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
