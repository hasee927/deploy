<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import { getPPOrderListApi } from '@/api/yinggao/orderMgr/proxypayorder'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import { ElSwitch, ElMessage  ,ElOption,
  ElOptionGroup,
  ElRadio,
  ElRadioButton,
  ElCheckbox,
  ElCheckboxButton,
  ElInput,
  ElMessageBox,
  ElIcon} from 'element-plus'
import { Search } from '@/components/Search'
import { FormSchema } from '@/components/Form'
import { ContentWrap } from '@/components/ContentWrap'
import Write from './components/Write.vue'
import Import from './components/Import.vue'
import BatchPayOut from './components/batchpayout.vue'
import { Dialog } from '@/components/Dialog'
// import { DictDetail, selectDictLabel } from '@/utils/dict'
// import { useDictStore } from '@/store/modules/dict'
import { BaseButton } from '@/components/Button'
import { getBigPayChannelOptionsApi, getSmallPayChannelOptionsApi } from '@/api/yinggao/merchantMgr/channel'
import { batchPayOutAmountApi, batchPayOutApi , batchSuccessApi, batchFailerApi, batchRevertPayOutApi,
		importBankDataApi, reissueNoticeApi, bankExportApi, batchChongZhengApi, batchCheckStatusApi, exportDataApi } from '@/api/yinggao/orderMgr/proxypayorder'

const auth = JSON.parse(localStorage.getItem("auth"))
const showOpertionMenu = ref(true)
const { t } = useI18n()

const changeShowMenu = async () => {
	if(auth.user.nickname == 'merchant'){
		showOpertionMenu.value = false
	}
}

changeShowMenu()


const { tableRegister, tableState, tableMethods } = useTable({
  // 获取代收订单列表
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
	
    const res = await getPPOrderListApi(jsonData)
    return {
      list: res.data || [],
      total: res.count || 0
    }
  },
  

})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList, delList, getSelections } = tableMethods
const selections = ref([] as any[])


const channelData = ref()

const getMaxPayChannel = async () => {
	const res = await getBigPayChannelOptionsApi();
	if (res) {
		const dataList = res.data
		dataList.map((item) =>{
			item.value = item.label
		})
		channelData.value = dataList
	}
}
getMaxPayChannel()


const tableColumns = reactive<TableColumn[]>([
	  {
	    field: 'selection',
	    type: 'selection',
	    show: true,
	    disabled: true
	  },	
	  {
	    field: 'order_id',
	    label: '订单ID',
	    show: true,
		width: '190px',
		fixed: 'left',
	  },
	  {
	    field: 'merchant_id',
	    label: '商户ID',
	    show: true,
		width: '80px'
	  },
	  {
	    field: 'orderNo',
	    label: '商户订单号',
	    show: true,
		width: '200px'
	  },
	  {
	    field: 'commission',
	    label: '手续费',
	    show: true,
	  	width: '100px'
	  },
	  {
	    field: 'amount',
	    label: '订单金额',
	    show: true,
		width: '110px'
	  },
	
	  {
	    field: 'status',
	    label: '订单状态',
	    show: true,
		width: '120px',
	    slots: {
	      default: (data: any) => {
	        const row = data.row
			//订单状态: pending:等待，success:成功，failed:失败, revert:恢复"
			if(row.status == 0) {
				return (<><span><el-button type="primary" size="small" plain>pending</el-button></span></>)
			}
			if(row.status == 1){
				return (<><span><el-button type="success" size="small" plain>success</el-button></span></>)
			}
			if(row.status == 2){
				return (<><span><el-button type="danger" size="small" plain>failed</el-button></span></>)
			}
			if(row.status == 3){
				return (<><span><el-button type="warning" size="small" plain>processing</el-button></span></>)
			}
			if(row.status == 4){
				return (<><span><el-button type="info" size="small" plain>revert</el-button></span></>)
			}
	      }
	    }
	  },
	
	  {
	    field: 'channel_code',
	    label: '通道code',
	    show: true,
		width: '120px'
	  },
	 //  {
	 //    field: 'amount_type',
	 //    label: '通道金额类型',
	 //    show: true,
		// width: '120px',
	 //  	slots: {
	 //  	  default: (data: any) => {
	 //  	    const row = data.row
	 //  		if(row.amount_type == 1) {
	 //  			return (<><span><el-button type="primary" size="small" plain>大金额</el-button></span></>)
	 //  		}else{
	 //  			return (<><span><el-button type="warning" size="small" plain>小金额</el-button></span></>)
	 //  		}
	 //  	  }
	 //  	}
	 //  },
	  {
	    field: 'utr',
	    label: 'UTR',
	    show: true,
	  	width: '160px'
	  },
	  {
	    field: 'ifsc',
	    label: 'ifsc',
	    show: true,
		width: '160px'
	  },
	  {
	    field: 'mode',
	    label: '付款模式',
	    show: true,
		width: '100px'
	  },
	  {
	    field: 'name',
	    label: '姓名',
	    show: true,
		width: '120px'
	  },
	  {
	    field: 'bank_account',
	    label: '银行卡号',
	    show: true,
		width: '180px'
	  },
	  {
	    field: 'phone',
	    label: '手机号',
	    show: true,
		width: '180px'
	  },
	
	  {
	    field: 'bank_msg',
	    label: '银行信息',
	    show: true,
		width: '160px'
	  },
	
	  {
	    field: 'create_datetime',
	    label: '创建时间',
	  	width: '200px',
	    show: true
	  },
	  {
	    field: 'pay_time',
	    label: '支付时间',
	    show: true,
	  	width: '200px'
	  },
	  {
	    field: 'action',
	    width: '330px',
	    label: '操作',
	    show: showOpertionMenu.value,
		fixed: 'right',
	    slots: {
	      default: (data: any) => {
	        const row = data.row
			const status = row.status
	        return (
				<>
			  
				<BaseButton v-show={status == 0}  type="primary" link size="small" onClick={() => showPayOut(row)} >出款</BaseButton>
				<BaseButton v-show={status == 3}  type="warning" link size="small" onClick={() => showPayOut(row)} >重新提交</BaseButton>
				<BaseButton v-show={status == 4}  type="primary" link size="small" onClick={() => batchChongZheng(row)} >冲正</BaseButton>
				<BaseButton v-show={status == 0 || status == 3} type="success" link size="small" onClick={() => batchSuccess(row)} >成功</BaseButton>
				<BaseButton v-show={status == 0 || status == 3}  type="danger" link size="small" onClick={() => batchFailer(row)} >失败</BaseButton>
				<BaseButton v-show={status != 0} type="primary" link size="small" onClick={() => ReissueNotice(row)} >补发通知</BaseButton>
				<BaseButton v-show={status == 3} type="primary" link size="small" onClick={() => batchStatus(row)} >状态检查</BaseButton>
	
	          </>
	        )
	      }
	    }
	  }
	])
	



const searchSchema = reactive<FormSchema[]>([
	
	
	{
		field: 'min_amount',
		label: '最小金额',
		component: 'Input',
		componentProps: {
		  clearable: false,
		  style: {
			width: '214px'
		  }
		}
	},
	{
		field: 'max_amount',
		label: '最大金额',
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
		label: '通道',
		component: 'Select',		
		componentProps: {
			style: {
			  width: '214px'
			},
			options: channelData,
		},
	  },

	
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
	},

  {
    field: 'order_id',
    label: '订单ID',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },

  {
    field: 'orderNo',
    label: '商户订单号',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'bank_account',
    label: '银行卡号',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'utr',
    label: 'UTR',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'status',
    label: '订单状态',
    component: 'Select',
    componentProps: {
      style: {
        width: '214px'
      },
      options: [
        {
          label: 'pending',
          value: "0"
        },
        {
          label: 'success',
          value: "1"
        },
		{
		  label: 'failed',
		  value: "2"
		},
		{
		  label: 'processing',
		  value: "3"
		},
		{
		  label: 'revert',
		  value: "4"
		}
      ]
    }
  },
  {
  	field: 'from_date',
  	component: 'DatePicker',
  	label: "选择时间",
  	componentProps: { type: 'datetimerange' }
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
const dialogVisibleImport = ref(false)
const dialogVisibleBatchPayOut = ref(false)
const dialogTitle = ref('')

const currentRow = ref()
const actionType = ref('')

const writeRef = ref<ComponentRef<typeof Write>>()
const importRef = ref<ComponentRef<typeof Import>>()
const batchpayoutRef = ref<ComponentRef<typeof BatchPayOut>>()
const saveLoading = ref(false)

const total_amount = ref(100)


const showPayOut =  async (data) => {

	if(data) {
		selections.value = [data]
	}else{
		selections.value = await getSelections()
	}
	
	if (selections.value.length > 0) {
		const res = await batchPayOutAmountApi(selections.value)
		
		if(res) {
			const data = {"total_amount": res.data, "failNum": 50}
			dialogTitle.value = '批量出款'
			currentRow.value = data
			dialogVisibleBatchPayOut.value = true
		}
	}else{
		return ElMessage.warning('请先选择数据！')
	}

}



// 批量出款
const batchPayOut = async () => {
	dialogVisibleBatchPayOut.value = false
	
	const write = unref(batchpayoutRef)
	var formData = await write?.submit()
	var pay_channel_code = ''
	var jsonData = {}
	var ids = []
	const failNum = formData['failNum']
	if (failNum) {
		if (!(/(^[1-9]\d*$)/.test(failNum))) {
　　　　　　 ElMessage({
				type: 'error',
				message: '输入的不是整数！',
			})
			return;
　　　　 }
	}

	if (formData['pay_channel_code']){
		pay_channel_code = formData['pay_channel_code']
	}

	if(pay_channel_code) {
		jsonData['pay_channel_code'] = pay_channel_code
		selections.value.map((item, index) => {
		  item['channel_code'] = pay_channel_code
		  item['failNum'] = failNum
		  ids.push(item['id'])
		});
		jsonData['ids'] = ids
		jsonData['data'] = selections.value
	}else {
		jsonData['pay_channel_code'] = pay_channel_code
		selections.value.map((item, index) => {
		  item['failNum'] = failNum
		  ids.push(item['id'])
		});
		jsonData['ids'] = ids
		jsonData['data'] = selections.value
	}
	
	await batchPayOutApi(jsonData)
	// if (res) {
	// 	if (res.code == 200) {
	// 		ElMessage({
	// 			type: 'success',
	// 			message: '批量出款成功',
	// 		})
	// 	}
	// }
	ElMessage({
		type: 'success',
		message: '提交出款数据成功！',
	})
	getList()
	
	
}



// 批量重新提交
const batchRevertPayOut = async (data) => {
	console.log("data---->>>>>", data)
	if (data) {
		ElMessageBox.confirm(
			'确定重新提交?',
			'系统提示',
			{
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning',
			}).then(async () => {
				data['failNum'] = 50
				const res = await batchRevertPayOutApi([data])
				if (res) {
					if (res.code == 200) {
						ElMessage({
							type: 'success',
							message: '重新提交成功',
						})
					}
				}
				getList()
				
				// if (res) {
				// 	if(res.code == 200){
				// 		ElMessage({
				// 			type: 'success',
				// 			message: '重新提交成功',
				// 		})
				// 	}else{
				// 		ElMessage({
				// 			type: 'error',
				// 			message: '重新提交失败',
				// 		})
				// 	}
				// 	getList()
				// }
				
				
			}).catch(() => {
				ElMessage({
					type: 'info',
					message: '取消出款',
				})
			})
	}else {
		selections.value = await getSelections()
		if (selections.value.length > 0) {
			const ret = await batchPayOutAmountApi(selections.value)
			ElMessageBox.prompt(
				'批量重新提交总金额是：'+ ret.data,
				'系统提示',
				{
					inputPlaceholder: '请输入重新出款失败数量限制，不输入默认50',
					confirmButtonText: '确定',
					cancelButtonText: '取消',
					type: 'warning',
				}).then(async ({value}) => {
					if (value) {
						if (!(/(^[1-9]\d*$)/.test(value))) {
				　　　　　　 ElMessage({
								type: 'error',
								message: '输入的不是整数！',
							})
							return;
				　　　　 }
					}

					if (!value) {
						value = '50'
					}
					
					selections.value.map(item => {
						item['failNum'] = value
					})
					
					const res = await batchRevertPayOutApi(selections.value)
					if (res) {
						if (res.code == 200) {
							ElMessage({
								type: 'success',
								message: '批量重新提交成功',
							})
						}
					}
					getList()
					
					// if (res) {
					// 	if(res.code == 200){
					// 		ElMessage({
					// 			type: 'success',
					// 			message: '批量重新提交成功',
					// 		})
					// 	}else{
					// 		ElMessage({
					// 			type: 'error',
					// 			message: '批量重新提交失败',
					// 		})
					// 	}
					// 	getList()
					// }
			
					
				}).catch(() => {
					ElMessage({
						type: 'info',
						message: '取消批量出款',
					})
				})
		
		} else {
			return ElMessage.warning('请先选择数据')
		}
	}
}



// 批量成功
const batchSuccess = async (data) => {
	console.log("data---->>>>>", data)
	if (data) {
		ElMessageBox.confirm(
			'确定成功?',
			'系统提示',
			{
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning',
			}).then(async () => {
				const res = await batchSuccessApi([data])
				if (res) {
					ElMessage({
						type: 'success',
						message: '成功',
					})
					getList()
				}
				
				
			}).catch(() => {
				ElMessage({
					type: 'info',
					message: '取消成功',
				})
			})
	}else {
		selections.value = await getSelections()
		if (selections.value.length > 0) {
		
			ElMessageBox.confirm(
				'确定批量成功?',
				'系统提示',
				{
					confirmButtonText: '确定',
					cancelButtonText: '取消',
					type: 'warning',
				}).then(async () => {
					const res = await batchSuccessApi(selections.value)
					if (res) {
						ElMessage({
							type: 'success',
							message: '批量成功',
						})
						getList()
					}
			
					
				}).catch(() => {
					ElMessage({
						type: 'info',
						message: '取消批量成功',
					})
				})
		
		} else {
			return ElMessage.warning('请先选择数据')
		}
	}
}



// 批量失败
const batchFailer = async (data) => {
	if (data) {
		ElMessageBox.confirm(
			'确定更改为失败?',
			'系统提示',
			{
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning',
			}).then(async () => {
				const res = await batchFailerApi([data])
				if (res) {
					ElMessage({
						type: 'success',
						message: '更改成功',
					})
					getList()
				}
				
				
			}).catch(() => {
				ElMessage({
					type: 'info',
					message: '取消更改失败',
				})
			})
	}else {
		selections.value = await getSelections()
		if (selections.value.length > 0) {
		
			ElMessageBox.confirm(
				'确定批量失败?',
				'系统提示',
				{
					confirmButtonText: '确定',
					cancelButtonText: '取消',
					type: 'warning',
				}).then(async () => {
					const res = await batchFailerApi(selections.value)
					if (res) {
						ElMessage({
							type: 'success',
							message: '批量成功',
						})
						getList()
					}
			
					
				}).catch(() => {
					ElMessage({
						type: 'info',
						message: '取消批量成功',
					})
				})
		
		} else {
			return ElMessage.warning('请先选择数据')
		}
	}
}



// 批量冲正
const batchChongZheng = async (data) => {
	console.log("data---->>>>>", data)
	if (data) {
		ElMessageBox.confirm(
			'确定冲正?',
			'系统提示',
			{
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning',
			}).then(async () => {
				const res = await batchChongZhengApi([data])
				if (res) {
					ElMessage({
						type: 'success',
						message: '成功',
					})
					getList()
				}
				
				
			}).catch(() => {
				ElMessage({
					type: 'info',
					message: '取消成功',
				})
			})
	}else {
		selections.value = await getSelections()
		if (selections.value.length > 0) {
		
			ElMessageBox.confirm(
				'确定批量冲正?',
				'系统提示',
				{
					confirmButtonText: '确定',
					cancelButtonText: '取消',
					type: 'warning',
				}).then(async () => {
					const res = await batchChongZhengApi(selections.value)
					if (res) {
						ElMessage({
							type: 'success',
							message: '批量成功',
						})
						getList()
					}
			
					
				}).catch(() => {
					ElMessage({
						type: 'info',
						message: '取消批量成功',
					})
				})
		
		} else {
			return ElMessage.warning('请先选择数据')
		}
	}
}




// 补发通知
const ReissueNotice = async (data) => {
	const res = await reissueNoticeApi(data)
	if(res) {
		if(res.code == 200) {
			ElMessage({
				type: 'success',
				message: '通知成功',
			})
		}
	}
}
 

// 银行出款
const bankPayExport = async () => {
	selections.value = await getSelections()
	if (selections.value.length > 0) {
		dialogTitle.value = '银行出款'
		dialogVisible.value = true
	} else {
		return ElMessage.warning('请先选择数据')
	}		
}

const bankPay = async (data) => {
	const write = unref(writeRef)
	const formData = await write?.submit()

	const ids = []
	selections.value.forEach((item, index) => {
	  ids.push(item.id)
	});

	formData['ids'] = ids
	// console.log("formData----->>>>>>", formData)
	
	try {
	  loading.value = true
	  const res = await bankExportApi(formData)
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
		getList()
	  }
	} catch (err) {
	  console.log('bankExportApi error')
	} finally {
	  loading.value = false
	}

}
 

const ImportData =  async () => {
	dialogVisibleImport.value = true	
}


// 导入文件
const uploadData = async () => {
	const write = unref(importRef)
	const formData = await write?.submit()
	// console.log("formData----->>>>>>", formData)
	
	// 
	const res = await importBankDataApi(formData)
	console.log(res)
	
	dialogVisibleImport.value = false
	getList()
}


// 批量状态检查
const batchStatus = async (data) => {

	if (data) {
	
		ElMessageBox.confirm(
			'确定状态检查！',
			'系统提示',
			{  
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning',
			}).then(async () => {
				const res = await batchCheckStatusApi([data])
				if (res) {
					if (res.code == 200) {
						ElMessage({
							type: 'success',
							message: '状态检查成功',
						})
					}
				}
				getList()
				
				// if (res) {
				// 	if(res.data.status == "Success"){
				// 		ElMessage({
				// 			type: 'success',
				// 			message: '状态检查成功',
				// 		})
				// 	}else{
				// 		ElMessage({
				// 			type: 'error',
				// 			message: '状态检查失败',
				// 		})
				// 	}
				// 	getList()
				// }
				
				
			}).catch(() => {
				ElMessage({
					type: 'info',
					message: '取消状态检查',
				})
			})
	}else {
		selections.value = await getSelections()
		if (selections.value.length > 0) {
			ElMessageBox.confirm(
				'确定批量状态检查！',
				'系统提示',
				{
					confirmButtonText: '确定',
					cancelButtonText: '取消',
					type: 'warning',
				}).then(async () => {	
					const res = await batchCheckStatusApi(selections.value)
					if (res) {
						if (res.code == 200) {
							ElMessage({
								type: 'success',
								message: '批量状态检查成功',
							})
						}
					}
					getList()
					// if (res) {
					// 	if(res.data.status == "Success"){
					// 		ElMessage({
					// 			type: 'success',
					// 			message: '批量状态检查成功',
					// 		})
					// 	}else{
					// 		ElMessage({
					// 			type: 'error',
					// 			message: '批量状态检查失败',
					// 		})
					// 	}
					// 	getList()
					// }
			
					
				}).catch(() => {
					ElMessage({
						type: 'info',
						message: '取消批量状态检查',
					})
				})
		
		} else {
			return ElMessage.warning('请先选择数据')
		}
	}
}


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

<!--        -->
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
	  :pagination="{total}"
      @register="tableRegister"
      @refresh="getList"
    >

	<template #toolbar>
        <ElRow :gutter="10">

          <ElCol :span="1.5" v-hasPermi="['auth.user.import']">
            <BaseButton type="primary" @click="showPayOut">批量出款</BaseButton>
          </ElCol>
          
          <ElCol :span="1.5" v-hasPermi="['auth.user.reset']">
            <BaseButton type="success" @click="batchSuccess">批量成功</BaseButton>
          </ElCol>
		  <ElCol :span="1.5" v-hasPermi="['auth.user.reset']">
		    <BaseButton type="danger" @click="batchFailer">批量失败</BaseButton>
		  </ElCol>
		  <ElCol :span="1.5" v-hasPermi="['auth.user.reset']">
		    <BaseButton type="warning" @click="showPayOut">批量重新提交</BaseButton>
		  </ElCol>
          <ElCol :span="1.5" v-hasPermi="['auth.user.reset']">
            <BaseButton type="primary" @click="batchChongZheng">批量冲正</BaseButton>
          </ElCol>
		  <ElCol :span="1.5" v-hasPermi="['auth.user.export']">
		    <BaseButton type="success"  @click="bankPayExport()">银行出款</BaseButton>
		  </ElCol>
          <ElCol :span="1.5" v-hasPermi="['auth.user.export']">
            <BaseButton type="danger" @click="ImportData">导入银行流水</BaseButton>
          </ElCol>
		  
		  <ElCol :span="1.5" v-hasPermi="['auth.user.import']">
		    <BaseButton type="primary" @click="batchStatus">批量状态检查</BaseButton>
		  </ElCol>
		  
		  <ElCol :span="1.5">
		    <BaseButton type="success" @click="exportQueryList">导出</BaseButton>
		  </ElCol>
		  
        </ElRow>
      </template>	  
	  
	  
    </Table>
  </ContentWrap>

	<Dialog v-model="dialogVisible" :title="dialogTitle" :height="160">
		<Write ref="writeRef" :current-row="currentRow" />

		<template #footer>
		  <BaseButton type="primary" :loading="saveLoading" @click="bankPay">
			出款
		  </BaseButton>
		  <BaseButton @click="dialogVisible = false">{{ t('dialogDemo.close') }}</BaseButton>
		</template>
	</Dialog>



	<Dialog v-model="dialogVisibleImport" :title="dialogTitle" :height="160">
		<Import ref="importRef" :current-row="currentRow" />

		<template #footer>
		  <BaseButton type="primary" :loading="saveLoading" @click="uploadData">
			导入
		  </BaseButton>
		  <BaseButton @click="dialogVisibleImport = false">{{ t('dialogDemo.close') }}</BaseButton>
		</template>
	</Dialog>
	
	
	<Dialog v-model="dialogVisibleBatchPayOut" :title="dialogTitle" :height="460">
		<BatchPayOut ref="batchpayoutRef" :current-row="currentRow" />
	
		<template #footer>
		  <BaseButton type="primary" :loading="saveLoading" @click="batchPayOut">
			出款
		  </BaseButton>
		  <BaseButton @click="dialogVisibleBatchPayOut = false">{{ t('dialogDemo.close') }}</BaseButton>
		</template>
	</Dialog>
	

	

  <!-- <AuthManage ref="authManageRef" :current-row="currentRow" @get-list="getList" /> -->
</template>
