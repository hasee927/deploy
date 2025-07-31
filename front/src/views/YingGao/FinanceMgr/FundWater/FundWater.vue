<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import { getFundWaterListApi, exportDataApi } from '@/api/yinggao/finance/fundwaterlist'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import { ElSwitch, ElMessage } from 'element-plus'
import { Search } from '@/components/Search'
import { FormSchema } from '@/components/Form'
import { ContentWrap } from '@/components/ContentWrap'
import { BaseButton } from '@/components/Button'

const auth = JSON.parse(localStorage.getItem("auth"))

const { t } = useI18n()

const { tableRegister, tableState, tableMethods } = useTable({
  // 获取资金流水列表
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
    const res = await getFundWaterListApi(jsonData)
    return {
      list: res.data || [],
      total: res.count || 0
    }
  },
  

  
})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList } = tableMethods



const tableColumns = reactive<TableColumn[]>([
  {
    field: 'id',
    label: '流水号',
    show: true,
	width: '100px'
  },
  {
    field: 'merchant_id',
    label: '商户ID',
    show: true,
	width: '100px'
  },
  {
    field: 'optime',
    label: '操作时间',
    show: true,
	width: '160px'
  },

  {
    field: 'water_type',
    label: '流水类型',
    show: true,
	width: '120px',
	slots: {
	  default: (data: any) => {
	    const row = data.row
		if(row.water_type == 0) {
			return (<><span><el-button type="warning" round size="small">划扣</el-button></span></>)
		}
		if(row.water_type == 1){
			return (<><span><el-button type="primary" round size="small">上分</el-button></span></>)
		}
		if(row.water_type == 2){
			return (<><span><el-button round size="small">可用转代付</el-button></span></>)
		}
		if(row.water_type == 3){
			return (<><span><el-button type="primary" round size="small">代付转可用</el-button></span></>)
		}
		if(row.water_type == 4){
			return (<><span><el-button type="success" round size="small">支付成功</el-button></span></>)
		}
		if(row.water_type == 5){
			return (<><span><el-button type="primary" round size="small">订单冲正</el-button></span></>)
		}
		if(row.water_type == 6){
			return (<><span><el-button type="info" round size="small">代付pending</el-button></span></>)
		}
		if(row.water_type == 7){
			return (<><span><el-button type="success" round size="small">代付成功</el-button></span></>)
		}
		if(row.water_type == 8){
			return (<><span><el-button type="danger" round size="small">代付失败</el-button></span></>)
		}
	  }
	}
  },

  {
    field: 'bill_no',
    label: '所属单号',
    show: true,
	width: '200px'
  },
  
  {
    field: 'change_amount',
    label: '变动余额',
    show: true,
	width: '120px'
  },
  
  {
    field: 'pending_amount',
    label: '在途金额变动',
    show: true,
	width: '120px'
  },
  
  {
    field: 'pay_amount',
    label: '代付金额变动',
    show: true,
	width: '120px'
  },
  
  {
    field: 'change_total_amount',
    label: '变动后总金额',
    show: true,
	width: '120px'
  },
	
  {
	field: 'change_pending_amount',
	label: '变动后在途金额',
	show: true,
	width: '140px'
  },
  
  {
    field: 'change_pay_amount',
    label: '变动后代付金额',
    show: true,
	width: '140px'
  },
  
  {
    field: 'change_fund',
    label: '变动后可转换金额',
    show: true,
	width: '140px'
  },
  

  {
    field: 'remark',
    label: '备注',
    show: true,
	width: '240px'
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
        width: '50px'
      }
    }
  },
  {
    field: 'bill_no',
    label: '所属单号',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '50px'
      }
    }
  },
  {
    field: 'water_type',
    label: '流水类型',
    component: 'Select',
    componentProps: {
      clearable: false,
      style: {
        width: '50px'
      },
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
		},
		{
		  label: '支付成功',
		  value: 4
		},
		{
		  label: '订单冲正',
		  value: 5
		},
		{
		  label: '代付pending',
		  value: 6
		},
		{
		  label: '代付成功',
		  value: 7
		},
		{
		  label: '代付失败',
		  value: 8
		},
		
	  ]
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


const dialogVisible = ref(false)
const dialogTitle = ref('')

const currentRow = ref()


const exportQueryList = async (data) => {
	const formData = searchParams.value

	try {
	  loading.value = true
	  const res = await exportDataApi(formData)
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
		    <BaseButton type="success" @click="exportQueryList">导出</BaseButton>
		  </ElCol>
        </ElRow>
      </template>
    </Table>
  </ContentWrap>
  <!-- <AuthManage ref="authManageRef" :current-row="currentRow" @get-list="getList" /> -->
</template>
