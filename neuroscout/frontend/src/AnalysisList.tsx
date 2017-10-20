/*
Resuable AnalysisList component used for displaying a list of analyses, e.g. on 
the home page or on the 'browse public analysis' page
*/
import * as React from 'react';
import { Button, Table } from 'antd';
import { Space } from './HelperComponents';
import { AppAnalysis } from './coretypes';
import Status from './Status';
import { Link } from 'react-router-dom';

export interface AnalysisListProps {
  loggedIn?: boolean;
  publicList?: boolean;
  analyses: AppAnalysis[];
  cloneAnalysis: (id: string) => void;
  onDelete?: (analysis: AppAnalysis) => void;
}

class AnalysisTable extends Table<AppAnalysis> {}

const AnalysisList = (props: AnalysisListProps) => {
  const { analyses, publicList, cloneAnalysis, onDelete } = props;

  // Define columns of the analysis table
  // Open link: always (opens analysis in Builder)
  // Delete button: only if not a public list and analysis is in draft mode
  // Clone button: any analysis
  const analysisTableColumns = [
    { title: 'ID', dataIndex: 'id' },
    {
      title: 'Name',
      render: (text, record: AppAnalysis) =>
        <Link to={`/builder/${record.id}`}>
          {record.name}
        </Link>
    },
    {
      title: 'Status',
      dataIndex: 'status',
      render: (text, record) => <Status status={record.status} />
    },
    { title: 'Modified at', dataIndex: 'modifiedAt' },
    {
      title: 'Actions',
      render: (text, record: AppAnalysis) =>
        <span>
          <Button type="primary" ghost={true} onClick={() => cloneAnalysis(record.id)}>
            Clone
          </Button>
          <Space />
          {!publicList &&
            record.status === 'DRAFT' &&
            <Button type="danger" ghost={true} onClick={() => onDelete!(record)}>
              Delete
            </Button>}
        </span>
    }
  ];
  return (
    <div>
      <AnalysisTable
        columns={analysisTableColumns}
        rowKey="id"
        size="small"
        dataSource={analyses}
        expandedRowRender={record =>
          <p>
            {record.description}
          </p>}
        pagination={analyses.length > 20}
      />
    </div>
  );

  /* Old card-based interface - Leaving it here but commented out in case we decide to go back to using cards instead of a table
  return (
    <Row type="flex" justify="center">
      <Col span={18}>
        {analyses!.map(analysis =>
          <div key={analysis.id}>
            <Card title={analysis.name} extra={<Status status={analysis.status} />}>
              <Row>
                <Col span={18}>
                  <p>
                    <strong>Description: </strong>
                    {analysis.description || 'N/A'}
                  </p>
                  <p>
                    <strong>Last modified: </strong>
                    {analysis.modifiedAt}
                  </p>
                  <br />
                </Col>
              </Row>
              <Row>
                <Col span={18}>
                  <Button
                    type="primary"
                    ghost={true}
                    onClick={() =>
                      message.warning(
                        'Analysis viewer not implemented yet. Try the Edit button to open analysis in Builder'
                      )}
                  >
                    View
                  </Button>
                  <Space />
                  {!publicList &&
                    <Button type="primary" ghost={true}>
                      <Link to={`/builder/${analysis.id}`}>Edit</Link>
                    </Button>}
                  <Space />
                  <Button type="primary" ghost={true} onClick={() => cloneAnalysis(analysis.id)}>
                    Clone
                  </Button>
                  <Space />
                  {analysis.status === 'DRAFT' &&
                    !publicList &&
                    <Button type="danger" ghost={true} onClick={() => onDelete!(analysis)}>
                      Delete
                    </Button>}
                </Col>
              </Row>
            </Card>
            <br />
          </div>
        )}
      </Col>
    </Row>
  ); */
};

export default AnalysisList;